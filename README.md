# DigitRecognizerWithAPI
This project is Flask App for digit recognizer using MNIST set and with a API to use.

## It is not real time detection, it will statically recognize the digits

This project will allow user to upload images those will be used to feed it to the model and also be saved in the library of the admin.
Some test images are in ```static\img\uploads``` folder.

```fulldrmodel.h5,fulldrmodel.json,kfulldrmodeldigit.h5 and kfulldrmodeldigit folder``` are all saved models in different formats. Refer
[fulldigitrecog.ipynb](https://github.com/HarshOza36/DigitRecognizerWithAPI/blob/master/fulldigitrecog.ipynb) for it.

[test.py](https://github.com/HarshOza36/DigitRecognizerWithAPI/blob/master/test.py "Api test") is used to test the API created in flask for that flask should be running first.


## How to use?
Download the Repository.

Open command line.

Open your folder where you have the extracted Downloaded Files.

**Step 1**
```
pip install virtualenv
```
**Step 2**
```
virtualenv env
```
here env is your environent name
```
source env/Scripts/activate     ->to activate our environment for UNIX
```

```
.\env\Scripts\activate      ->to activate our environment for Windows
```

to activate our environment

**Step 3**
```
pip install -r requirements.txt
```
To install dependencies

**Step 4**
```
python app.py
```
