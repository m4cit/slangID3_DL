# slangID3 DL
slangID3 DL tries to identify slang phrases via Deep Learning models created with PyTorch.

You can train a selection of classifiers, and print out a test set of phrases with the **DEMO** button.
Or you can pass a phrase and see what type it, and the individual words are identified as. All the available models are pre-trained, but you can re-train if needed.


## Gallery

### Icon

<img src='https://raw.githubusercontent.com/m4cit/slangID3_DL/main/misc/gallery/slangID3_dl_icon.png' height="120">


### Prediction

<img src='https://raw.githubusercontent.com/m4cit/slangID3_DL/main/misc/gallery/slangID3_dl_pd.png' width="900">


### Demo

<img src='https://raw.githubusercontent.com/m4cit/slangID3_DL/main/misc/gallery/slangID3_dl_dm.png' width="900">


## How to run slangID3 DL
1. Install Python **3.10** or newer.
2. Install PyTorch with `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`
(might be different for linux)
4. Install the required packages by running `pip install -r requirements.txt` in your shell of choice. Make sure you are in the project directory.
5. Run `python slangID3_DL.py`

**Note:** It might take a while to load. Be patient.


## Usage
You can predict with the included pre-trained models, and re-train if needed.

Preprocessing is the last step before training a model.

If you want to use the original dataset **_data.csv_** after some changes, or the augmented dataset **_augmented_data.csv_**, use the preprocessing function before training.


## Performance
There is currently two models available:

* **NeuralNet_2l_lin:** Neural Network with 2 linear layers
* **NeuralNet_4l_relu_lin:** Neural Network with 4 linear layers and 3 ReLU layers

The best **F<sub>1</sub> score is ~71.4% with model NeuralNet_2l_lin**

**Note:** Score on the test set with the best parameters within 100 epochs of training, with the original training data.


## Issues
- The training dataset is still too small, resulting in overfitting (after augmentation).
- Reproducibility is an issue with regard to training.


## Preprocessing
The preprocessing script removes the slang tags, brackets, hyphens, and converts everything to lowercase.


## Augmentation
I categorized the slang words as:
* \<pex> personal expressions
  * _dude, one and only, bro_
* \<n> singular nouns
  * _shit_
* \<npl> plural nouns
  * _crybabies_
* \<shnpl> shortened plural nouns
  * _ppl_
* \<mwn> multiword nouns
  * _certified vaccine freak_
* \<mwexn> multiword nominal expressions
  * _a good one_
* \<en> exaggerated nouns
  * _guysssss_
* \<eex> (exaggerated) expressions
  * _hahaha, aaaaaah, lmao_
* \<adj> adjectives
  * _retarded_
* \<eadj> exaggerated adjectives
  * _weirdddddd_
* \<sha> shortened adjectives
  * _on_
* \<shmex> shortened (multiword) expressions
  * _tbh, imo_
* \<v> infinitive verb
  * _trigger_

(not all tags are available due to the small dataset)


## Source of the data
Most of the phrases come from archive.org's [Twitter Stream of June 6th](https://archive.org/details/archiveteam-twitter-stream-2021-06).


## Recognition of Open Source use
* PyTorch
* scikit-learn
* customtkinter
* pandas
* numpy
* tqdm

