# Deep image python api

## Usage

### Install pipenv
```
sudo apt install pipenv
```

### Usage

* You need to replace API_TOKEN with your real api token from https://deep-image.ai/my-profile/ in example commands below.

### Run transform script with human like properties
```
python transform.py -f examples/test.jpg --upscale 2 --enhance --denoise --token API_TOKEN
```

### Run transform script with certain transformation types
```
python transform.py -f examples/test.jpg -tp ganzoom2-jpg90,ganenhance1-jpg90 --token API_TOKEN
```

