FROM public.ecr.aws/lambda/python:3.8
RUN pip3 install requests bs4 boto3
# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "scrape_website.handler" ]