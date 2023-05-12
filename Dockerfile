# Select the desired python image
FROM ...

# Copy the required files
COPY ...

# Install your environment using pip - here your package
RUN ...

# Expose a port to the api reachable
EXPOSE 80:80

# Execute your API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]