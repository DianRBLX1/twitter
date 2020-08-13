FROM python:3.8-alpine
RUN apk update
RUN apk add git
RUN apk add --update --no-cache g++ gcc libxslt-dev libxml2-dev

RUN mkdir /Transtale-tweet-bot && chmod 777 /Transtale-tweet-bot
ENV PATH="/Transtale-tweet-bot/bin:$PATH"
WORKDIR /Transtale-tweet-bot

RUN git clone https://github.com/nishanksisodiya/Transtale-tweet-bot /Transtale-tweet-bot
RUN pip install -r requirements.txt

#
# Copies session and config(if it exists)
#
#COPY ./sample_config.env ./userbot.session* ./config.env* /One4uBot/

#
# Finalization
#
CMD ["python3" ,"bots/translateTweet.py"]