# python-hrpt

Read NOAA HRPT binaries and output images, all in python!

The input is synchronized and derandomized CADU (not really, more like N-KLM) frames. The output is imagery in 16-bit PNG format for AVHRR channels, and 3x8 bit color format for the composite. 

# Format

The satellites NOAA-15, 18 and 19 transmit on L band a non-CCSDS compatible 666kbaud stream that contains imagery directly from the satellite. This tool decodes the raw binary data into imagery

![AVHRR-221](https://github.com/radio-satellites/python-hrpt/assets/114111180/a59521cf-e19b-493e-ba62-501a26c14e70)
