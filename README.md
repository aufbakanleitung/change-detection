# Detect Changes on Website
This program loads a page periodically and checks if there are any changes to it compared to the given value.
It can do this by hashing the site, or if that is not possible, by checking a specific element using Pythons webscraper: BeautifulSoup 

Deploy this program to AWS Lambda as a zip:
```commandline
pip install --target ./package requests boto3 bs4
cd package; zip -r ../change-detect-lambda.zip .
cd ..; zip -g change-detect-lambda.zip lambda_function.py
aws lambda create-function --function-name change-detect --zip-file fileb://change-detect-lambda.zip --handler lambda_function.lambda_handler --runtime python3.8 --role arn:aws:iam::331730032056:role/lambda-website-change-detect
```
[See documentation](https://docs.aws.amazon.com/lambda/latest/dg/python-package-create.html) 

The Lambda is periodically triggered with EventBridge, using a cronjob (every 5 min): `cron(*/5 6-23 * * ? *)`.
It is sending this JSON as input:
```json
{
  "url": "https://www.piccardthof.nl/huisjes-te-koop/",
  "check_line": "<h6>Er zijn op dit moment geen huisjes te koop</h6>",
  "original_element": "h6"
}
```

Deploy this program as a Docker container:
```commandline
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 331730032056.dkr.ecr.eu-west-1.amazonaws.com
docker tag website-change-detect:latest 331730032056.dkr.ecr.eu-west-1.amazonaws.com/website-change-detect:latest
docker push 331730032056.dkr.ecr.eu-west-1.amazonaws.com/website-change-detect:latest
```
