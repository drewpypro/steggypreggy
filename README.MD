# steggypreggy 
![steggypreggy](eggydatapreggy.png)

# Purpose
- Fertilize gifs with json data. 🥚
- Harvest json data out of gifs. 🐣

# Usage

```
# git clone https://github.com/drewpypro/steggypreggy
# cd steggypreggy
# python3 steggypreggy.py -e -i data.json -f skeleton.gif -o skelly_crypt.gif
✅ Data successfully embedded in frame 13 of skelly_crypt.gif
# python3 steggypreggy.py -d -i skelly_crypt.gif
✅ Extracted data successfully saved to extracted_data.json
# cat extracted_data.json
[
    "mysecretisinmygif"
]
#
```