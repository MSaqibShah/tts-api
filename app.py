from flask import Flask, request
from pymongo import MongoClient


# CONSTANTS

# define the base URL for the audio files
AUDIO_URL_BASE = "http://172.16.1.209:8000/"
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'audio_db'
MONGO_COLLECTION = 'audio_collection'


# create a MongoClient instance
client = MongoClient(MONGO_HOST, MONGO_PORT)

# connect to the database
client = client[MONGO_DB]

# connect to the collection

collection = client[MONGO_COLLECTION]

# create a Flask app
app = Flask(__name__)


@app.route('/get_audios', methods=['GET'])
def get_all():
    try:
        # get all the documents from the collection
        documents = collection.find({})
        # create a list to store the documents
        docs = []
        # iterate over the documents
        for doc in documents:
            # remove the _id field from the document
            doc.pop('_id')
            # create the audio URL
            audio_url = AUDIO_URL_BASE + doc['msisdn']
            doc['audio_url'] = audio_url
            # append the document to the list
            docs.append(doc)
        # return the list of documents as a JSON response
        return {'audios': docs}
    except Exception as e:
        return {'error': str(e)}


@app.route('/get_audio/<msisdn>', methods=['GET'])
def get_one(msisdn):
    try:
        # get the document from the collection
        document = collection.find_one({'msisdn': msisdn})
        if document is None:
            return {'error': 'No document found with the given MSISDN'}
        # remove the _id field from the document
        document.pop('_id')
        # create the audio URL
        audio_url = AUDIO_URL_BASE + document['msisdn']
        document['audio_url'] = audio_url
        # return the document as a JSON response
        return document
    except Exception as e:
        return {'error': str(e)}


@app.route('/synthesize_audio', methods=['GET'])
def transcribe_audio():
    try:
        # get text from body
        text = request.args.get('text')
        # write the code for actually creating text-to-speech here
        # hopin the data that comes back is in the format of a dictionary

        data = {

            "text": "नमस्ते, Sachin Vithal Hogar यह कॉल आपके Bajaj Auto Finance लोन के संबंध में है. आपकी Bajaj Auto Finance loan की किस्त 4925 रुपये 3 july 2023 को देय है. हम आपसे अनुरोध कर रहे हैं कि नियत तिथि से पहले अपने खाते में पर्याप्त शेष राशि बनाए रखें. पुष्टि करने के लिए 1 दबाएँ. धन्यवाद.",

            "speech_rate": 0.91,

            "use_stress": "False",

            "quality": 20,

            "msisdn": "112233",

            "voiceCode": "hi_f1"

        }

        return data

    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    app.run()
