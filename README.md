# s2RSS - RSS Feed Generator

## Project Progress

### 0.1 - Groundwork

-   [x] Flask project setup
-   [x] User accounts
-   [x] Login, signup, index, 404 and 500 pages
-   [x] Figure out feed format
-   [x] Simple "create feed" (title, link, desc)
-   [x] Simple feed generation function
-   [x] PoC Search Patterns
-   [x] Advanced "create feed"
-   [x] Preview in "create feed"
-   [x] Document `fetch-address`, `fetch-pattern-result` etc...
-   [x] Errors to the log file
-   [ ] Optimize the API calls from create-feed, do we really need to send the source 3 times?

### 0.2 - Scaling

-   [ ] Implement queueing for the `fetch-address`
-   [ ] Handle regex matches that takes too long
-   [ ] Change to Atom feeds

### 0.3 - UI/UX

-   [ ] Format the code after `fetch-address` to make it more readable

## Project Timeline

**2023-10-21**

-   `1021 - 1042` Hello World
-   `1042 - 1145` User Accounts
-   `1145 - 1201` Figure Our Project Structure
-   `1202 - 1230` Simple "Create Feed"
-   `1233 - 1256` Simple Feed Generation
-   `1351 - 1422` Write Usage Documentation
-   `0749 - 0901` Write PoC Search Patterns (too much regex)
-   `0901 - 0923` Bug Fixes in the PoC

**2023-10-23**

-   `1007 - 1123` Basic Web Implementation

**2023-10-25**

-   `1740 - 1903` Create Feed Page All Done
-   `1912 - 2030` Working MPV Done
-   `2035 - 2144` Documentation

**2023-10-26**

-   `2230 - 2320` Final Touches

**2023-10-27**

-   `1400 - 1543` Final Touches and Bug Fixes
-   `1604 - 1650` Edit and Delete Feeds

## Known Problems

-   ~~Application is currently vulnerable to regex DoS attacks~~ (still needs more testing)
-   Only works on static websites
-   ~~Does not work with a single item element match, must be 2 or more~~
-   CSRF is possible for deleteing feeds if the attacker knows the feed id

## Usage

Default credentials: `admin:12345678`

Each item in your RSS feed will have 3 main properties, author, title, link and content.
To extract this data from the website we will use search patterns, for example let's
look at something like HackerNews (I know it already has RSS), here is the source code
of random HN post

```html
...
<tr class="athing" id="38035672">
	<td align="right" valign="top" class="title">
		<span class="rank">1.</span>
	</td>
	<td valign="top" class="votelinks">
		<center>
			<a id="up_38035672" href="vote?id=38035672&amp;how=up&amp;goto=news"
				><div class="votearrow" title="upvote"></div
			></a>
		</center>
	</td>
	<td class="title">
		<span class="titleline"
			><a
				href="https://mathstodon.xyz/@tao/111287749336059662"
				rel="noreferrer"
				>Lean4 helped Terence Tao discover a small bug in his recent
				paper</a
			><span class="sitebit comhead">
				(<a href="from?site=mathstodon.xyz"
					><span class="sitestr">mathstodon.xyz</span></a
				>)</span
			></span
		>
	</td>
</tr>
<tr>
	<td colspan="2"></td>
	<td class="subtext">
		<span class="subline">
			<span class="score" id="score_38035672">155 points</span> by
			<a href="user?id=gridentio" class="hnuser">gridentio</a>
			<span class="age" title="2023-10-27T07:25:32"
				><a href="item?id=38035672">4 hours ago</a></span
			>
			<span id="unv_38035672"></span> |
			<a href="hide?id=38035672&amp;goto=news">hide</a> |
			<a href="item?id=38035672">52&nbsp;comments</a>
		</span>
	</td>
</tr>
<tr class="spacer" style="height:5px"></tr>
...
```

Let's start building our item search pattern we can ommit all the content we don't
care about using `{*}`, we still have to keep some of the code identifying the elemnt
around it so our program can know exactly what you are looking for, notice how we kept
some elements with classes around our targets, note that we
do need the post ID, you will see why later

```html
{*}
<tr class="athing" id="38035672">
	{*}
	<td class="title">
		<span class="titleline">
			<a
				href="https://mathstodon.xyz/@tao/111287749336059662"
				rel="noreferrer"
				>Lean4 helped Terence Tao discover a small bug in his recent paper</a>
			{*}
	<span class="score" id="{*}"></span> by
		<a href="user?id=gridentio" class="hnuser">gridentio</a>
	</td>
</tr>
{*}
```

Now that we have just the information we need, we can use our search pattern symbol `{%}`
to find the items we care about, then we can construct out final item title, link and
content

```html
<tr class="athing" id="{%}">
	{*}<span class="titleline"
		><a href="{%}" {*}>{%}</a>{*}<a href="user?id={%}" class="hnuser"></a
	></span>
</tr>
```

As you can see, we used search patterns for 3 values, the post id, the link and the title
our values must look like this

```bash
{%1}: 38035672
{%2}: https://mathstodon.xyz/@tao/111287749336059662
{%3}: Lean4 helped Terence Tao discover a small bug in his recent paper
{%4}: gridentio
```

Now you can see how we will construct our item properties, we can do something like this

```bash
title = {%3} by ~{%4}
link = https://news.ycombinator.com/item?id={%1}
content = {%2}
```

It's that simple, you use the search pattern to find information, and then you use
it to construct your item properties however you like
