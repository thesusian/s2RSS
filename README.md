# s2RSS - RSS Feed Generator

## Project Progress

### 0.1 - Groundwork

-   [x] Flask project setup
-   [x] User accounts
-   [x] Login, signup, index, 404 and 500 pages
-   [x] Figure out feed format
-   [x] Simple "create feed" (title, link, desc)
-   [x] Simple feed generation function
-   [ ] PoC Search Patterns
-   [ ] Advanced "create feed"
-   [ ] Preview in "create feed"

## Project Timeline

**2023-10-21**

-   `1021 - 1042` Hello World
-   `1042 - 1145` User Accounts
-   `1145 - 1201` Figure Our Project Structure
-   `1202 - 1230` Simple "Create Feed"
-   `1233 - 1256` Simple Feed Generation
-   `1351 - 1422` Write Usage Documentation
-   `0749 - 0901` Write PoC Search Patterns (too much regex)

## Known Problems

Application is currently vunerable to regex DoS attacks

## Usage

Each item in your RSS feed will have 3 main properties, author, title, link and content.
To extract this data from the website we will use search patterns, for example let's
look at something like HackerNews (I know it already has RSS), here is the source code
of random HN post

```html
...
<tr class="athing" id="37965142">
	<td align="right" valign="top" class="title">
		<span class="rank">1.</span>
	</td>
	<td valign="top" class="votelinks">
		<center>
			<a id="up_37965142" href="vote?id=37965142&amp;how=up&amp;goto=news"
				><div class="votearrow" title="upvote"></div
			></a>
		</center>
	</td>
	<td class="title">
		<span class="titleline"
			><a
				href="https://unixsheikh.com/articles/we-have-used-too-many-levels-of-abstractions-and-now-the-future-looks-bleak.html"
				rel="noreferrer"
				>We have used too many levels of abstractions and now the future
				looks bleak</a
			><span class="sitebit comhead">
				(<a href="from?site=unixsheikh.com"
					><span class="sitestr">unixsheikh.com</span></a
				>)</span
			></span
		>
	</td>
</tr>
<tr>
	<td colspan="2"></td>
	<td class="subtext">
		<span class="subline">
			<span class="score" id="score_37965142">218 points</span> by
			<a href="user?id=riidom" class="hnuser">riidom</a>
			<span class="age" title="2023-10-21T08:42:52"
				><a href="item?id=37965142">2 hours ago</a></span
			>
			<span id="unv_37965142"></span> |
			<a href="hide?id=37965142&amp;goto=news">hide</a> |
			<a href="item?id=37965142">118&nbsp;comments</a>
		</span>
	</td>
</tr>
...
```

Let's start building our item search pattern we can ommit all the content we don't
care about using `{*}`, we still have to keep some of the code identifying the elemnt
around it so our program can know exactly what you are looking for, notice how we kept
some elements with classes around our targets, note that we
do need the post ID, you will see why later

```html
{*}
<tr class="athing" id="37965142">
	{*}
	<td class="title">
		<span class="titleline">
			<a
				href="https://unixsheikh.com/articles/we-have-used-too-many-levels-of-abstractions-and-now-the-future-looks-bleak.html"
				rel="noreferrer"
				>We have used too many levels of abstractions and now the future
				looks bleak</a>
			{*}
	<span class="score" id="{*}"></span> by
		<a {*}>riidom</a>
		<span {*}></span>
	</td>
</tr>
{*}
```

Now that we have just the information we need, we can use our search pattern symbol `{%}`
to find the items we care about, then we can construct out final item title, link and
content

```html
{*}<tr class="athing" id="{%}">{*}<td class="title"> <span class="titleline"> <a href="{%}" rel="noreferrer">{%}</a>{*} by {*}class="hnuser">{%}</a>
```

As you can see, we used search patterns for 3 values, the post id, the link and the title
our values must look like this

```bash
{%1} = 37965142
{%2} = https://unixsheikh.com/articles/we-have-used-too-many-levels-of-abstractions-and-now-the-future-looks-bleak.html
{%3} = We have used too many levels of abstractions and now the future looks bleak
{%4} = riidom
```

Now you can see how we will construct our item properties, we can do something like this

```bash
author = {%4}
title = {%3}
link = https://news.ycombinator.com/item?id={%1}
content = https://unixsheikh.com/articles/we-have-used-too-many-levels-of-abstractions-and-now-the-future-looks-bleak.html
```

It's that simple, you use the search pattern to find information, and then you use
it to construct your item properties however you like
