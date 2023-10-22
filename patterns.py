import re
from bs4 import BeautifulSoup as bs

HTML="""
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
"""
HTML = re.sub(r'[\t\n]', ' ', HTML)
HTML = re.sub(r' +', ' ', HTML)
HTML = re.sub(r'(?<=>)(?=<)', ' ', HTML)
HTML = re.sub(r'\s*(?=>)', '', HTML)

PATTERN ="""{*}<tr class="athing" id="{%}">{*}<td class="title"> <span class="titleline"> <a href="{%}" rel="noreferrer">{%}</a>{*} by {*}class="hnuser">{%}</a>{*}"""
PATTERN = re.sub(r' +', ' ', PATTERN)
PATTERN = re.sub(r'\s*{%}\s*', '(.*?)', PATTERN)
PATTERN = re.sub(r'\s*\{\*\}\s*', '.*', PATTERN)
PATTERN = re.sub(r'(?<=>)(?=<)', ' ', PATTERN)
PATTERN = re.sub(r'\s*(?=>)', '', PATTERN)

userPattern = PATTERN.replace("/", "\/")

print("HTML: "+HTML)
print("REGEX: "+userPattern)

regex = r''+userPattern
matches = re.findall(regex, HTML, re.DOTALL)

# Printing the results
print("Regexed:")
for match in matches:
    print("* {"+str(match)+"}")