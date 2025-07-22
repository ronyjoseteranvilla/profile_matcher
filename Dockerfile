# Install slim version of Python
FROM python:3.13.0-slim

# Set-up virtual environment folder
ENV VIRTUAL_ENV=.venv
RUN python -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/Scripts:$PATH"

# Install Dependencies
COPY . .
RUN pip install -r requirements.txt


# Run application
CMD [ "python", "src/app.py" ]

