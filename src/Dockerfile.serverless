FROM public.ecr.aws/lambda/python:3.10

RUN pip3 install pipfile-requirements==0.3.0
RUN yum -y install git

COPY . ${LAMBDA_TASK_ROOT} 
WORKDIR ${LAMBDA_TASK_ROOT}

ARG GIT_TOKEN

COPY ./Pipfile.lock .
RUN pipfile2req ./Pipfile.lock -s > requirements.txt
RUN pip3 install -r requirements.txt

CMD ["app.main.app"]