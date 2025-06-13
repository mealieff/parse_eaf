# First download: /mfa model download g2p english_us_arpa
## Generate the dictionary

Run the following command to create a dictionary using your corpus and the downloaded G2P model:

```bash
mfa g2p ~/mfa_data/my_corpus english_us_arpa ~/mfa_data/new_dictionary_lmk.txt
```

Optionally specify the number of alternate pronunciations with ```--num_pronunciations 3```