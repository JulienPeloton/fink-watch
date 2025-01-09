# Fink watch

This repository contains the script to display the number of alerts per night processed by Fink in real-time. The watch uses a raspberry pi to control the LCD Display Module, and get alert information from the Fink Kafka cluster.

## Display

<p float="center">
  <img src="pictures/watch_240_ztf.png" width="240" />
  <img src="pictures/watch_240_rubin.png" width="240" /> 
</p>

![watch](pictures/watch_desk.JPG)

## Usage

```bash
python app.py -h
usage: app.py [-h] [--local] [-width WIDTH] [-height HEIGHT] [-display DISPLAY]
              [-observatory OBSERVATORY] [-alert_per_deg ALERT_PER_DEG]

Launch the Fink watch

options:
  -h, --help            show this help message and exit
  --local               If specified, display on the local computer instead of the LCD
                        screen
  -width WIDTH          Width size in pixels. Default is 240
  -height HEIGHT        Height size in pixels. Default is 240
  -display DISPLAY      What to display on screen: watch, logo. Default is watch.
  -observatory OBSERVATORY
                        Name of the observatory to set the local time for the `clock`
                        option.
  -alert_per_deg ALERT_PER_DEG
                        Number of alerts per degree (for the alertmeter). Default is 1000
```

## Local testing

You can ...


```bash
python app.py --local
```


## Deployment on a Raspberry



## Acknowledgments

- Waveshare
- @HG for providing the name!
