# Notes

## Tuesday 11/12

### API: Application Programming Interface
- published set of protocols that can be used to have your program interact with another program/service

### REST APIs:
- **Re**presentational **S**tate **T**ransfer
- a REST API transmits data back after receiving an http(s) request
- returned data can be in various formats
  - most common are HTML, XML, JSON
- often require a **key**
  - mainly to limit service and prevent spamming with quotas

### Making a REST call in Python2 (and parsing response)
```python
import urlib2
data = urllib2.urlopen(nycsnowday.com)
```
- json library facilitates work with JSON data
  - .loads() turns a JSON object string into a dictionary
    - `d = json.loads(<STRING>)`
  - .dumps() turns python dict into JSON object string
    - `w = json.dumps(<DICT>)`