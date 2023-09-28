This is my recommender system project
This is the food recommendation system:

# To run the file
1. input the desired photo into merge/image/0
2. open combined_model.ipynb and restart and run all
3. open recommendation_result.ipynb and restart and run all
4. see the final result at the bottom of recommendation_result.ipynb

# preinstall
pip install -r requirement.txt

# your directory should contains the following folder:
- recommedation system
    - README.md
    - requirement.txt

    - image (image model)
        - photos (storing the yelp photo data)
        - image (storing the train, test, validate photo data)
            - train
            - test
            - validate 
        - image_CNN_model_baseline.ipynb (baseline model)
        - image_CNN_model_improve.ipynb (improved model)
        - photo_data_process.ipynb (create classes for photo data for CNN model)
        - processed_photo.csv
        - photo_to_dir.ipynb (put photo into corresponding class)

    - text (text model)
        - text_data_processed.ipynb (prepare data for LSTM model)
        - test_LSTM_model.ipynb (LSTM model)
        - Train_label.txt (training dataset)
        - Train_nolabel.txt (unlabel dataset)
        - Test.txt (test dataset)

    - rating (rating model)
        - rating_MLP_model_baseline.ipynb (baseline model)
        - rating_MLP_model_improve.ipynb (improved model)
        - rating_processed_data.ipynb (prepare data for MLP model)

    - merge (combine three model)
        - image
            - 0 (input photo for recommendation here)
        - combined_model.ipynb (combine three model together)
        - recommendation_result.ipynb (plotting the result)
        - final.csv (the final recommendation result)
        - Test1.txt (generated during recommendation - containing restaurant review for the recommendations)

    - yelp (storing yelp data)
        - process_data.ipynb (perform data cleaning and data processing of yelp data)
        - processed.csv
