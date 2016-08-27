# instagram-statistics
<img src="https://travis-ci.org/ahmdrz/instagram-statistics.svg?branch=master" />

Instagram Statistics using python and mustache

### Dependency

1. requests
2. pystache
3. bootstrap
4. jquery

**Instagram-API is forked from [this](https://github.com/LevPasha/Instagram-API-python) repository but converted from python3 to python2**

Please read the original [source code](https://github.com/LevPasha/Instagram-API-python)

### How to use

First of all you should replace your username and password in this line :

```python
  insta = Instagram("USERNAME", "PASSWORD")
```

or you can use it more easier

```bash
  python insta.py <username> <password>
```

After that , The program will be replace your instagram info in the template file and will make a new html file called output.html 

### License
See full license on [this](https://github.com/ahmdrz/instagram-statistics/blob/master/LICENSE) , Under GNU GENERAL PUBLIC LICENSE
