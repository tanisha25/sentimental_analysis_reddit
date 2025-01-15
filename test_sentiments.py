import pytest
from flask import Flask
from app import create_app, db
from app.models import SentimentAnalysis
from app.analysis import analyze_sentiment
from app.fetch_reddit import fetch_reddit_data
from unittest.mock import patch


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_sentiments.db'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_analyze_sentiment():
    posts = [
        {
            "content": "I am looking for subcontracting job in computer programming and data sciences. I have many years of quantitative analysis experience in private sector working with large dataset using C++ / Python and machine learning, plus project management. This is my first time looking into this area. Any suggestion will be much appreciated. I am US citizen.",
            "title": "Looking for subcontracting job in computer programming and data sciences"
        },
        {
            "title": "[Hiring] [Remote] [India] - Software Engineer I\n",
            "content": "* Experience : 1+ years\n* Skills : GoLang, Python, Java, NodeJS, TypeScript, REST APIs\n\n**Check more details and apply -**\n\n[https://peerlist.io/company/c2fo/careers/software-engineer-i/jobhmql89q79dolk63d8q8jgamjmpr](https://peerlist.io/company/c2fo/careers/software-engineer-i/jobhmql89q79dolk63d8q8jgamjmpr)\n\n",
        }
    ]
    results = analyze_sentiment(posts)
    assert len(results) == 2
    assert results[0]['sentiment'] == 'POSITIVE'
    assert results[1]['sentiment'] == 'POSITIVE'


def test_analyze_route(client):
    with patch('app.fetch_reddit.fetch_reddit_data') as mock_fetch:
        mock_fetch.return_value = [
           {"content": "Hello! I applied for the Laurea Magistrale in Music and Acoustic Engineering (Cremona campus) during the early bird phase. I submitted my application at the end of November, and it has been in the \"dossier under evaluation\" status since December 12th. Has anyone else applying to this program received any feedback yet?",
                        "title": "Acceptance Updates for Laurea Magistrale in Music and Acoustic Engineering"},
            {
                "content": "Recently started using a NAS to store personal stuff on it and I wanted to transfer all the photos that I kept on a 1tb hardrive in the past. There are 12886 items in total. First time transfering there where about 400 that failed. Solved by writing a quick python script to manually upload all the missing files. The problems is that one didn't upload. While writing another py script to check for the missing file the program retursn about 50 files all already on the network drive. Is the 1 file a calculation error or is there a way to fix it?\n\n  \nScripts:  \nReupload missing files and Missing file check in this order\n\n    import os\n    import shutil\n    \n    # Path to the local directory with files\n    local_directory = \"Source\"\n    \n    # Path to the mounted network drive\n    network_directory = \"Destination\"\n    \n    # Iterate over all files in the local directory\n    for file_name in os.listdir(local_directory):\n        local_file_path = os.path.join(local_directory, file_name)\n        network_file_path = os.path.join(network_directory, file_name)\n    \n        # Skip directories and only process files\n        if os.path.isfile(local_file_path):\n            # Check if the file already exists on the network drive\n            if os.path.exists(network_file_path):\n                print(f\"File already exists on server: {file_name}\")\n            else:\n                try:\n                    # Copy the file to the network drive\n                    shutil.copy2(local_file_path, network_file_path)\n    \n                    # Verify upload success by checking if the file exists on the network drive\n                    if os.path.exists(network_file_path):\n                        print(f\"Successfully uploaded: {file_name}\")\n                    else:\n                        print(f\"Upload failed: {file_name}\")\n                except Exception as e:\n                    print(f\"Error uploading {file_name}: {e}\")\n        else:\n            print(f\"Skipping non-file item: {file_name}\")\n    \n\n    import os\n    \n    # Paths to local directory and network drive\n    local_directory = \"Source\"\n    network_directory = \"Destination\"\n    \n    # Get lists of files in both directories\n    local_files = set(os.listdir(local_directory))\n    network_files = set(os.listdir(network_directory))\n    \n    # Find the missing file(s)\n    missing_files = local_files - network_files\n    \n    if missing_files:\n        print(\"Missing files:\")\n        for file in missing_files:\n            print(file)\n    else:\n        print(\"All files are accounted for.\")\n\n  \n  \n",
                "title": "One singular files refuses to transfer and I don't know how to find it."
            }

        ]
        response = client.post('/api/sentiment/analyze', data={'topic': 'programming', 'num_records': 2})
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert 'POSITIVE' in data
        assert 'NEGATIVE' in data

def test_database_integration(client):
    with client.application.app_context():
        new_record = SentimentAnalysis(
            topic='science',
            title = "I go to Loyola Maryland and don't know what to major",
            content = "I enjoy Finance and tech. I was aiming to make the most money out of college and was stuck between data science or Finance. Any help?",
            sentiment='POSITIVE',
            score=0.5994
        )
        db.session.add(new_record)
        db.session.commit()

        record = SentimentAnalysis.query.filter_by(topic='science').first()
        assert record is not None
        assert record.sentiment == 'POSITIVE'




def test_invalid_input(client):
    response = client.post('/api/sentiment/analyze', data={})
    assert response.status_code == 400
    assert 'Topic is required' in response.data.decode('utf-8')
