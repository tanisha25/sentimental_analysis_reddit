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
            title= "So, apparently Most IPV-related single suicides were of men who perpetrated nonfatal IPV  ",
            content = "[https://www.sciencedirect.com/science/article/pii/S2352827322000581](https://www.sciencedirect.com/science/article/pii/S2352827322000581)\n\n>It remains unclear how often and under what circumstances intimate partner violence (IPV) precedes suicide. Available research on IPV and suicide focuses largely on homicide-suicide, which is a rare event (<2% of suicides). We focus instead on single suicides (i.e., suicides unconnected to other violent deaths), which are the most common type of fatal violence in the US.Unfortunately, information about IPV circumstances is often unavailable for suicides. To address this gap, we sought to identify the proportion of single suicides that were preceded by IPV in North Carolina (NC), to describe the prevalence of IPV victimization and perpetration as precursors to suicide, and to explore how IPV-related suicides differ from other suicides. We used data from the NC Violent Death Reporting System (2010–2017, n = 9682 single suicides) and hand-reviewed textual data for a subset of cases (n = 2440) to document IPV circumstances.We had robust inter-rater reliability (Kappa: 0.73) and identified n = 439 IPV-related suicides. Most were males who had perpetrated nonfatal IPV (n = 319, 72.7%) prior to dying by suicide. Our findings suggest that IPV was a precursor for at least 4.5% of single [suicides.Next](http://suicides.Next), we conducted logistic [regression analyses](https://www.sciencedirect.com/topics/psychology/regression-analysis) by sex comparing IPV-related suicides to other suicides. For both men and women, IPV was more common when the person who died by suicide had recently disclosed suicidal [intent](https://www.sciencedirect.com/topics/psychology/intention), was younger, used a firearm, and was involved with the criminal legal system, even after controlling for covariates. We also found sex-specific correlates for IPV circumstances in suicide.Combined with homicide-suicide data (reported elsewhere), IPV is likely associated with 6.1% or more of suicides overall. Results suggest clear missed opportunities to intervene for this unique subpopulation, such as suicide screening and referral in IPV settings (e.g., batterer intervention programs, Family Justice Centers) that is tailored by sex.\n\n[https://www.sciencedirect.com/science/article/abs/pii/S1054139X24004531#:\\~:text=Among%20IPV%2Drelated%20suicides%2C%20most%20decedents%20were%20male%20and%20were%20described%20as%20IPV%20perpetrators.%20Physical%20IPV%20was%20most%20frequently%20reported.](https://www.sciencedirect.com/science/article/abs/pii/S1054139X24004531#:~:text=Among%20IPV%2Drelated%20suicides%2C%20most%20decedents%20were%20male%20and%20were%20described%20as%20IPV%20perpetrators.%20Physical%20IPV%20was%20most%20frequently%20reported)\n\n>Among IPV-related suicides, most decedents were male and were described as IPV perpetrators. Physical IPV was most frequently reported. Compared to decedents with a history of IPV perpetration, decedents with a history of IPV victimization were more often female and younger. Narratives of IPV victim decedents had higher odds of reporting physical IPV; narratives of IPV perpetrator decedents had higher odds of reporting psychological IPV.\n\nAny counter-studies?",
            sentiment='NEGATIVE',
            score=-0.9971
        )
        db.session.add(new_record)
        db.session.commit()

        record = SentimentAnalysis.query.filter_by(topic='science').first()
        assert record is not None
        assert record.sentiment == 'NEGATIVE'




def test_invalid_input(client):
    response = client.post('/api/sentiment/analyze', data={})
    assert response.status_code == 400
    assert 'Topic is required' in response.data.decode('utf-8')
