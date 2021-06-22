FROM python:3.9.5-alpine3.13

# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Bundle app source
COPY . /app

RUN pip install -r requirements.txt
RUN pip install gunicorn

# Install ExifTool
RUN apk add perl
RUN tar xzf Image-ExifTool-12.23.tar.gz && rm -fr Image-ExifTool-12.23.tar.gz

# Set non root user
RUN adduser -D user -h /home/user -s /bin/bash user
RUN chown -R user:user /home/user
RUN chmod -R 755 .

USER user
ENV HOME /home/user
ENV PATH ${PATH}:/app/Image-ExifTool-12.23

EXPOSE 5000
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "index:app" ]
