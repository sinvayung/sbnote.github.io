# 7 Python Regular Expressions Examples – Re Match Search FindAll

Regular expressions as a concept is not exclusive to Python at all.

Python, however, does have some nuances when it come to working with regular expressions.

This article is part of a series of articles on Python Regular Expressions.

In the first article of this series, we will focus on discussing how we work with regular expressions in python, highlighting python specifics.

We are going to introduce the methods we can use to perform queries over strings in Python. We’ll then talk about how we can use grouping to work with sub-parts of the matches we found using our queries.

The package we are interested in using to work with regular expressions in python is appropriately named ‘re’.

```
  >>> import re
```

### 1. Raw Strings in Python

The python parser interprets ‘\’ (backslashes) as escape characters in string literals.

If the backslash is followed by a special sequence recognized by the parser, the whole escape sequence is replaced by a corresponding special character (for example, ‘\n’ is replaced by a newline character when processed by the parser).



This behavior causes a problem when working with regular expressions in python because the ‘re’ package also uses backslash characters to escape special regex characters (like * or +).

The combination of these two behaviors would mean that sometimes you would have to escape escape characters themselves (when the special character was recognized by both the python parser and the regex parser), yet other times you would not (if the special character was not recognized by the python parser).

Rather than bend our brains trying to figure out how many backslashes we need, we can instead use raw strings.

A raw string is created by simply adding an ‘r’ character before the opening quote of a normal string. When a string is raw, the python parser will not even attempt to make any substitutions within it. Essentially, you are telling the parser to completely leave your string alone.

```
  >>> string = 'This is a\nnormal string'
  >>> rawString = r'and this is a\nraw string'
  >>> print string
  This is a
  normal string
  >>> print rawString
  and this is a\nraw string
```

### Performing Queries with Regex in Python

The ‘re’ package provides several methods to actually perform queries on an input string. The methods that we will be discussing are:

- re.match()
- re.search()
- re.findall()

Each of the methods accepts a regular expression, and string to scan for matches. Lets take a look at each of these methods in a little more detail to see how they work and how they differ.

### 2. Find Using re.match – Matches Beginning

Lets first take a look at the match() method. The way the match() method works is that it will only find matches if they occur at the start of the string being searched.

So for example, calling match() on the string ‘dog cat dog’, looking for the pattern ‘dog’ will match:

```
  >>> re.match(r'dog', 'dog cat dog')
  <_sre.SRE_Match object at 0xb743e720<
  >>> match = re.match(r'dog', 'dog cat dog')
  >>> match.group(0)
  'dog'
```

We’ll be talking more about the group() method in a little bit. For now, just know that when called with 0 as it’s argument, the group() method returns the pattern matched by the query.

I’m also glossing over the returned SRE_Match object for now, we’ll talk about that in a minute too.

But, if we call match() on the same string, looking for the pattern ‘cat’, we won’t:

```
  >>> re.match(r'cat', 'dog cat dog')
  >>>
```

### 3. Find Using re.search – Matches Anywhere

The search() method is similar to match(), but search() doesn’t restrict us to only finding matches at the beginning of the string, so searching for ‘cat’ in our example string finds a match:

```
  search(r'cat', 'dog cat dog')
  >>> match.group(0)
  'cat'
```

The search() method, however, stops looking after it finds a match, so search()-ing for ‘dog’ in our example string only finds the first occurrence:

```
  >>> match = re.search(r'dog', 'dog cat dog')
  >>> match.group(0)
  'dog'
```

### 4. Get Using re.findall – All Matching Objects

The querying method that I use by far the most in python though is the findall() method. Rather than being returned match objects (we’ll talk more about match objects in a little bit), when we call findall(), we simply get a list of all matching patterns. For me, this is just simpler. Calling findall() on our example string we get:

```
  >>> re.findall(r'dog', 'dog cat dog')
  ['dog', 'dog']
  >>> re.findall(r'cat', 'dog cat dog')
  ['cat']
```

### 5. Use match.start and match.end Methods

So, what exactly are these ‘match objects’ that search() and match() gave us earlier?

Rather than simply return the matching portion of the string, search() and match() return ‘matches’, which are essentially a wrapper around the matching substring.

You saw earlier that I could get to the matching substring by calling the matches group() method, (match objects are actually pretty useful when it comes to working with grouping, as we will see in the next section), but the match object also contains much more information about the matching substring.

For example, the match object can tell us the start and end indexes of the matching content from the original string:

```
  >>> match = re.search(r'dog', 'dog cat dog')
  >>> match.start()
  0
  >>> match.end()
  3
```

Knowing information like this can sometimes be very useful.

### 6. Group by Number Using match.group

As I mentioned earlier, match objects come in very handy when working with grouping.

Grouping is the ability to address certain sub-parts of the entire regex match. We can define a group as a piece of the regular expression search string, and then individually address the corresponding content that was matched by this piece.

Let’s look at an example to see how this works:

```
  >>> contactInfo = 'Doe, John: 555-1212'
```

The string I just created resembles a snippet taken out of someones address book. We can match the line with a regular expression like this one:

```
  >>> re.search(r'\w+, \w+: \S+', contactInfo)
  <_sre.SRE_Match object at 0xb74e1ad8<
```

By surrounding certain parts of the regular expression in parentheses (the ‘(‘ and ‘)’ characters), we can group the content and then work with these individual groups.

```
  >>> match = re.search(r'(\w+), (\w+): (\S+)', contactInfo)
```

These groups can be fetched using the match object’s group() method. The groups are addressable numerically in the order that they appear, from left to right, in the regular expression (starting with group 1):

```
  >>> match.group(1)
  'Doe'
  >>> match.group(2)
  'John'
  >>> match.group(3)
  '555-1212'
```

The reason that the group numbering starts with group 1 is because group 0 is reserved to hold the entire match (we saw this earlier when we were learning about the match() and search() methods)

```
  >>> match.group(0)
  'Doe, John: 555-1212'
```

### 7. Grouping by Name Using match.group

Sometimes, especially when a regular expression has a lot of groups, it is impractical to address each group by its number. Python also allows you to assign a name to a group using the following syntax:

```
  >>> match = re.search(r'(?P<last>\w+), (?P<first>\w+): (?P<phone>\S+)', contactInfo)
```

When can still fetch the grouped content using the group() method, but this time specifying the names we assigned the groups instead of the numbering we used before:

```
  >>> match.group('last')
  'Doe'
  >>> match.group('first')
  'John'
  >>> match.group('phone')
  '555-1212'
```

This makes for much more explicit and readable code. You can imagine that as the regular expression became more and more complicated, understanding what was being captured by a grouping would get harder and harder. Assigning names to your groups explicitly informs you and your readers of your intentions.

Grouping can be used with the findall() method too, even though it doesn’t return match objects. Instead, findall() will return a list of tuples, where the Nth element of each tuple corresponds to the Nth group of the regex pattern:

```
  >>> re.findall(r'(\w+), (\w+): (\S+)', contactInfo)
  [('Doe', 'John', '555-1212')]
```

However, named grouping doesn’t work when using the findall() method.

In this article we’ve introduced the basics of working with regular expressions in Python. We’ve learned about raw strings (and the headaches that they can save you when working with regular expressions). We’ve also learned how to perform basic queries using the match(), search(), and findall() methods, and even how to work with sub-components of a match using grouping.

As always, to find out more about this topic, the Python Official documentation on [re package](https://docs.python.org/2/library/re.html) is a great resource.

In future articles, we’ll dive deeper into regular expressions in Python. We’ll talk about how we can capture an even broader range of matches, how we can use them to make substitutions within a string, and how we can even use them to parse python data structures out of text files.

[原文](https://www.thegeekstuff.com/2014/07/python-regex-examples/)  [中文译文](http://blog.jobbole.com/74844/)