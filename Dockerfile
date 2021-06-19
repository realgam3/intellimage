FROM python:3.9-slim

# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Bundle app source
COPY . /app

RUN pip install -r requirements.txt
RUN pip install gunicorn

# Install ExifTool
RUN tar xzf Image-ExifTool-12.23.tar.gz && rm -fr Image-ExifTool-12.23.tar.gz

# Set non root user
RUN useradd -c "user" -m -d /home/user -s /bin/bash user
RUN chown -R user:user /home/user
RUN chmod -R 755 .

USER user
ENV HOME /home/user
ENV PATH ${PATH}:/app/Image-ExifTool-12.23

EXPOSE 5000
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "index:app" ]
