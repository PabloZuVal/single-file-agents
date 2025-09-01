# OpenAI Agent Disruption
what's up Engineers Andy Dev Dan here something I think about a lot is how can
we maximize our compute usage with powerful AI agents while steering clear
of the road map of companies like open AI when open AI releases an agent
1,256 startups are immediately destroyed eviscerated for example if you were
building a research agent open AI deep research just ate your breakfast lunch
and dinner imagine all your time engineering resources and time investment vanished instantly cooked
from startups to individual Engineers it doesn't matter how great your work is or
how far you've scaled your AI coding or what technical Innovation you found if you invest in the wrong agent in the
wrong tool in the wrong product you're at risk of Getting bulldozed By open Ai and other gen tech companies so how can
we stay ahead and build powerful effective agents while staying out of
the way of the generative AI road map I spent a lot of time in this space and I
want to share a pattern with you for building powerful lean compute gobbling
AI agents that can help you move fast iterate and scale your compute usage
while staying out of the way then near the end of this video we're going to discuss why we care about agents so much
and I'll explain why I and other engine engers are so obsessed with agents
agents are everything and I'll explain why in this video by using astrals
all-in-one python tool UV and by combining it with powerful AI coding
techniques we can build and deploy single file
[Applause] agents so what do a single file agent
# Single File Agents
and how does it help us move fast scale our compute and avoid getting disrupted by big tech companies I have this simple
project here in cursor and right away you'll notice something weird we only
have two files we have a file database and a python file so before we dive into
the agent architecture let's just run our agent with UV and let me show you how powerful this single file is UV run
SFA single file agent DD analytics. database will pass in that database
file- P for prompt list all tables and their columns - c Let's us set the
compute that our agent can use we'll set this to 10 let's kick off our duck DB AI
agent you see here it's kicking off the first compute Loop and it only needed one shot to complete this you can see we
have a single function argument call you can see we're using the rich python library to format the output here this
agent in particular is powered by open AI 03 mini so what just happened there
how was I able to pack in so much intelligence and capability into a single python file we're going to dive
into that in just a second but I want to show you the full agentic loop that our agent can go through so let's run this
again but let's ask our duck DB AI agent to do something more complex for us I'm going to say users score greater than 80
and Status active Okay so you can see here this is the wrong table name um it
has to figure out where these columns are coming from and what the exact name of these columns are okay so so there's a lot that I'm kind of leaving up to our
agent to figure out and it's going to run that exact same pattern right so we now have an agent Loop only this time
it's going to take a more iterative approach so you can see there it's listing tables it found the user table
it then is running this describe table arguments tool call so that I can understand what this table looks like
there's the output for that and then at the end here it's running Run final SQL query this is the final tool call the
final function call and we can see the exact query it's running and the exact outputs we have an AI agent that is
adept at operating duck DB local databases so this is super powerful as a
series of tools at its disposal it can use to solve the problem of information
Discovery to understand the structure of the database and then it has full autonomy right up to 10 compute Loops to
solve the problem and return the results to us we're using multiple libraries inside of a single file so how is this
possible we have to give credit to astrals UV you can think of this as bun
for python it's the all-in-one python ecosystem manager it basically replaces
every other python tool and most importantly for us for these powerful single file agents it gives us this
ability run scripts with support for inline dependency metadata let's dive
into this feature right now so we can see how we're building out these powerful single file agents
#Astral UV Single File Scripts
so if we open up our duct DB open aai Agent here you can see right at the top
of this file something fascinating right we have dependencies you know you saw
with this single command here right we had UV run this creates a Sandbox
environment this allows us to run the script as a standalone file with these dependencies included so we have open AI
rich and pantic so this is the first key aspect of the single file agent structure we need to be able to load and
use dependencies from any python Library most importantly we need a model
provider right so now we have this we have access to this and our single file agent now what does the agentic
structure look like for this agent you can see we're using pantic to create our argument structure so for instance for
our list table args we have the model pass in reasoning this is a powerful pattern to help you understand what your
language model was thinking at every single step if we open up every one of these tool argument structures I'm
always requesting reasoning you can see it there you can see it there so on and so forth right so that's a super
important pattern you can use when building your agents always pass in reasoning and then always log the
reasoning so you can see we have tools we have the agent prompt but the most important thing is the agentic loop down
here so let's go ahead and break this down and then let's go ahead and look at how we can distribute this pattern with
AI coding to scale it up to an entirely new AI agent so at the start here we're
pulling in all of our arguments we have our- D for database - P for prompt - c for compute we have our open AI key
check here we're then making our database path Global so that every single function can access it we're
building our prompt and then we're running the main agentic Loop so this is where all the magic happens this is
where we give our AI agent full control to run tools run functions gather
feedback build up its context and solve the problem problem we once solved let's open this up so we're doing our compute
Loop check here and then as you can imagine we're running our intelligence so we're using 03 mini you can see here
we're requiring a tool call with every Loop we want our llm to execute a tool
we're then looking for Tool calls once we find a tool which we should always have we are running our process of
determining which tool to select you can build any type of structure any type of map you want to handle this I'm just
doing this with the simplest pattern possible here we just have a bunch of if statements that parse the arguments and
then call the function we then take the result and we pass it back in to the language model right we pass it back
into to our context window very importantly here we also have an exception so if something goes wrong
inside of the tool we're also passing this back to the model right we want our agent to just solve the problem right we
want to design a great prompt we want to design great tools and then just hand off the problem to our agent we go off
we go on about day we go you know solve other specific problems and then in parallel it's solving this problem that
we gave it really well thanks to our clean agent design so this is one agent
pattern that I'm working with but I want to point out something that's really powerful here you saw the list tables
described sample but we also have this run test SQL query and Run final SQL
query from the tech ecosphere you may have picked up on this idea of verifiable domains and closed loop
systems this is something that we talk about about in principled AI coding specifically for the AI coding domain
but it really applies to all agentic technology we can do something interesting here with this run test SQL
query let's go ahead and open up the arguments and you can see here it looks the exact same as our Run final SQL
query and we can go ahead and fire off our agent again and just take a look to see if it's actually going to kick off
this call sometimes it completely skips the run test SQL query because it just doesn't need it it doesn't need the test
but we can you can do something like this create a new table high score users
from the user table and select all users with score greater than 80 that are
active and 2025 let's pass it off to our duck DB AI agent and just see how it
does with this I'm also going to kick up the compute Loops just in case it needs a little bit more energy let's kick that off and let's see how it does here so
you can see it's first validating the structure right it needs to find the tables so it's running list tables it's
seeing the schema structure of that table it's now running this test SQL
command so it's verifying that what we're going to ask for will work instead of you know looking for human in the
loop feedback or instead of running the final query what it's doing here is running this test SQL query this is a
really important pattern for building out great agents you don't have to wait to close the loop to let your agent
fully validate the process right so I have this run test SQL it's running this internally
adding more information to its context window you know gathering information about how to solve the problem of you
know creating this query creating this new table and then finally after it's validated it it's then running this
final query here right so after validation it's now saying you know we can take this query it's safe it works
it looks good let's go ahead and run this final query and create this new table so now of course if we hit up and
we hit up again let's get a smaller command to work with and we just say you know list all tables and one sample Row
for each table and we fire that off we should now get this brand new high score
so there's the high score users and the users table so this is fantastic right there's the sample our AI agent is
understanding these table structures it's understanding what we want and what we want to do and then it's giving us
you know these concrete outputs and you can see here how important it is to have the reasoning inside your agents right
it is explaining the results we're getting back here in a really concise way and this is really cool you can see
in the reasoning it's saying the sample Row from user and high scores is exactly the same so it's just going to return
the top result okay so this is really powerful I hope you can see that you know single file agents are powerful but
having a great AI agent structure with the right tools and the right order is
equally as powerful right it doesn't matter if you can build an agent it matters if you can build an effective
agent shout out to anthropic for writing you know this great post post on building effective agents this document
contains a lot of really key information I brought it up several times on the channel I think it encapsulates a lot of the key ideas and serves as a great
starting point for building out agents right they kind of end their story here with agents with this simple Loop right
which is effectively all in Asian is you have an llm call environment to an llm call and then they stop kind of whenever
they need to but all the magic happens in this Loop right happens in this
agentic Loop and this is where you know many struct structures can take place this is where many fortunes will be made
and lost uh you know due to just going after the wrong thing going after the wrong idea and you know again this is
why I want to bring this up the single fall agents enable us to build lean compute machines you don't want to
overinvestment
of top goto use cases for agents I think that's important but uh this is why I
bring up this pattern of building lightweight lean single file agents so
that you don't overinvestment so this is an important
pattern I think pre verification is just as important as post verification or closed loop verification um like I
mentioned this is something we talk about in principal a coding more on that later in the video having a test command
run and then a final command run whatever your domain specific problem is if your domain is verifiable I highly
recommend you check out this pattern of giving your agent tools to solve the
problem but also tools to prever verify that the answer that they're going to give you is the correct answer all right
and so that's what we're doing here with our duck DB single file agent so so what's the next step with this right we
have these powerful single pile agents with a great agentic structure that can solve problems for us we're going to
need many different types of AI agents not just this one right we're going to need for instance an SQL light agent how
can we take this agent and the agent structure and basically duplicate it you know make a couple tweaks to it so we
can scale and reuse our single file agent pattern right with this powerful tooling thanks to astral UV we now churn
out these powerful condensed air agents so you know how can we do that we all already know the answer to this
especially if you've been with the channel or if your eyes are open in the tech ecosystem at all right now we can
do this with AI [Applause]
# AI Coding Agents With Aider
coding so now that we have this agent working in a single file with a great
agent pattern and all dependencies encapsulated we can iterate at light speed with powerful AI coding techniques
many of which we've discussed in principled AI coding we're overdue for
AI coding on the channel so let's go ahead and write up a concise AI coding spec prompt to create a new SQL light
single file agent and then I'll pitch principled AI coding for those who aren't aware of what it is and how it
can accelerate your engineering I also have some updates coming for existing members we're going to have some nice
lightweight tooling to help us utilize all the principles we learned inside the course so more than that in a second
let's first build out our SQL light AI agent so this is going to be relatively
simple since duck DB and SQ SQL light are very very similar what we'll do here is open the terminal we'll type CP SFA
we'll basically just copy this create an SQL light version light great I'm also going to touch AI code. sh and this is
where we're going to build out our context model and prompt so that we can quickly reuse our single file agent
pattern in a reusable scalable way I use AER as my primary AI coding Workhorse
you can deploy this pattern with any AI coding tool you want of course you cursor wind Surfer Klein whatever your
deal is go ahead and hop into that I like to use AER and cursor side by side and let me show you a new pattern and
let me also just kind of you know share some of the advantages you get when you use a a coding tool like ader so I'm
just going to paste this in here since I've done this a million times let's start with just this blob here okay so
we're passing in our prompt as the first argument we're kicking off AER I want to run the 03 Mini model in architect mode
with the high reasoning effort this is some of the best computer you can get right now I want claw 3.5 Sonet to make
the edits that 03 mini suggests and then we have a couple of configurations here just to speed things up and then in my
context you can see I'm passing in I want every single python file available as the context okay and then finally the
message is just going to be the prompt so whatever we pass in here we can you know run this now we can say sh Ai and
then just pass in whatever prompt and then we can start getting AI coding changes in on this right let me show you
a little hint of what I have coming for principled a coding members there's a big theme right now about scaling
compute usage and just throwing more compute at the problem and then your problem will be solved you know
basically just by turning up the knob we can see that this is true even for AI coding this is going to look really
stupid but you're going to understand how powerful this is as we work through this I'm later going to copy this
command I'm going to paste it here so let me turn off cursor tab so we can write this by ourselves here I'm going
to say double check all changes requested to make sure they've been
implemented and that's it and so what we end up with here is a prompt chain of length four right we have an architect
drafting the changes and then an editor writing the changes and then again we have an architect double-checking all
the changes that just happened in a brand new instance and then we have an Editor to write those changes right to
write anything that was you know potentially missed fantastic so now we're going to actually write the prompt this is going to be really simple I'm
going to get the path to this I'm just going to say update and then I'll say refactor to Target SQL light
databases keep all functions the same but Target SQL light databases with SQL
light 3 so I'm being specific about what library I want use here update tools and prompt to reference SQL
light okay because if we open up this file you can see here if we just search duct DB we have you know many references
you can see on the side here we have many references to duct B so that's it that's the prompt I'm going to copy this
and I have this kind of reusable AI coding configuration right you can think of this as a kind of just generic a
coding um script that we can call that runs a compute enhanced AI coding chain
of assistants right we have two AER assistants in architect mode we're just going to copy this we do dollar sign PB
paste that's it so this is going to update it's going to kick off two AI coding assistants running back to back
this is our first shot and this is our our reflection step right all right so
there we go we're getting our changes we're updating our tool calls to reference SQ light instead of duct DB
and then at some point here we're going to see our prompt get updated so you can see there all those tools that looks
great we on Final SQL query now we're referencing SQL light instead of duct DB you can see we had an update in the
prompt and now we're running the reflection right so remember the reflection is literally just this double
check all changes requested and then we're pasting The Prompt in again so let's see what happens now we've already
taken one shot at architect and editor with AER and now we're running again so
you can see here look at how many things were missed right we have the architect saying hey you missed this here hey you
missed this here and then the editor is coming in and actually Chang those things right so we can now search SQL
light and so we should see a bunch of references to SQL light now with that new syntax you know as a test we can
also come in here and search duck DB right so this is really good we don't see any references to duck DB anymore
more fantastic um and now we should be able to run our SQL light agent just as
we did our duct DB open AI agent so in order to do that we need to pull in an SQL light version of this I'll paste
this in and you can see my SQL light extension uh showing this table here
right so this is our user's table let's go and close this so we now have this ready for our new SQL light agent let's
go ahead and save this and now let's just run our SQL light agent SFA single pile agent and we're going to run our
SQL light version - D analytics SQL light database - P list five rows from
user table and for our compute we'll just say five right should be pretty simple so far so good right our code
compile so that looks great we have our first tool call that looks awesome there it is so SQL light uh running just like
our duck DB did we're getting a you know slightly different output format because of course we're using SQL light we were
able to reuse our existing single file agent architecture we made an update to it with a clean prompt chain of length
four where every prompt was us kicking off AER we have an architect and then an editor and then we just basically
doubled it right our reflection actually saved us you know a little bit of energy this idea of scaling up your compute
really does translate to almost anywhere you're using language models anywhere you're running a prompt right even if
it's embedded inside of a tool like AER right you have to remember all these tools right cursor AER chat GPT Claude
right every one of these tools at the end is is running the new fundamental unit of knowledge work it's all about
the prompt and agents is how we scale The Prompt up this is how we scale up
our impact at the beginning I said we would talk about you know why is everyone so obsessed with agents this is
why it's because agents lets us scale up our compute usage and then the age of
generative AI when you scale your compute you scale your impact this is a
big theme on The Andy Deb Dan Channel right now in q1 2025 the most important thing we can do is
figure out how to scale our compute agents are the name of the game you just saw what we did here with a duck DB you
know domain specific Focus agent with only five tools right it gathers context
it understands the structure it then internally validates for hard problems
and then it gives us the final result right when we take astral's UV and the ability to package dependencies in these
isolated s single file agents right these single file scripts this really lets us move fast scale our compute and
get work done and solve problems fast without overinvestigation
gather contexts to solve that specific problem you're trying to solve all right this is the key um this codebase is
going to be linked in the description for you drop the like drop the sub and you know drop a comment let me know how
deep into agents you are right now are you on the surface are you you know trying to understand agent structures
are you using any agents right now and you know let me know what you think about this idea to build out these
single file agents that you can quickly reuse and redeploy with help of you know
whatever your favorite AI coding tooling is at a high level the longer your prompt chain the more compute you're
using right and when we think about it what's happening in this agent Loop that we're running here in both our sqlite
and our open AI version you know what's happening here we can kick this off again let's go ahead and ask another question here let's list five users GT
greater than status archived or pending all right let's kick that off and
fantastic so we can see that we we have status archived or pending age is always over 30 right and this is running in
this agentic loop it's solving this problem automatically it has the tools it needs to do the job and you know
something I want to mention here you can think about an agent as a elongated prompt chain right it's a series of
prompt calls over and over and over again targeting a specific domain problem and it's all about figuring out
how to best solve that problem with the compute that you give it and so if an error URS Cur here we would probably
need to give you know more compute more uh you know Loops we're running 03 mini
is a powerful reasoning model so you know as it's thinking through what tools to call and solving these problems it's doing an extraordinary job an
interesting way to think about the AI agent is that the more compute you're giving it basically what we're doing is we're extending the prompt chain right
we're elongating the number of compute runs that it has so if we wanted to solve a really hard problem for instance
you know open ai's deep research tool this thing runs for for 5 to 30 minutes
right so you can imagine you know its compute Loop is you know blasted up to like 100 across various tools various
functions you know various capabilities that's a really powerful idea we're going to be looking into more on the
channel like I mentioned I'm going to have these single file agents in a codebase for you to check out tweak and
make your own I'll add a couple additional versions here that I was playing with so that you can you know check them out and build out your own I
have a version where I have the meta prompt we've talked about on the channel in inside of a single file agent you can
just quickly query your uh meta prompting agent to generate a new prompt for you things are moving fast agents
# Principled AI Coding
are here one of the most important agents and one of the most important things you can do right now is learn how
to write code with AI and not just learn but really scale your capabilities with
writing code with AI many of you on the channel you've already dove in to principled a coding let me just pitch
this for those who haven't taken it yet this is really important and I want to make sure I'm sharing this tool so that
everyone is understanding the State Engineering is in and how they can progress keep up and thrive in the new
world of generative AI so principal AI coding is my take on how to transition
from the old ways of engineering to the new way we now have over a thousand Engineers that have taken principal a
coding that have a New Perspective and actionable patterns and principles they can use for their Engineering in today's
landscap ape of generative Ai and more importantly for the next wave of generative AI based engineering so you
know I don't know if you've noticed um if your eyes are open you've probably noticed this but software engineering has changed and it's time to change with
it a coding is the largest productivity multiplyer for engineers to ever exist this is something that you can't miss
out on okay if you miss out on this you'll be left behind I think 2025 is the last year where you can write code
without Ai and really be used useful right really be employable really be uh
able to contribute in a meaningful way go on Twitter for 5 seconds go on Reddit and you know just type in a coding type
in cursor type in AER um type in Klein like type in any one of these tools and
you'll understand that there are Engineers um all the way from Noob beginners to senior expert principal
bigname Engineers right that you you know likely look up to they understand this curve right they understand these
two curves you're are either using the tool that helps you scale your impact or you're not okay and you know just to say
it really bluntly if you're not writing code with AI if you're still manually coding you are not using the best tool
for the job anymore if you're writing code with AI you are absolutely on an upward curve okay principal a coding was
built to help you make this transition in the shortest amount of time possible okay the only thing better than
experience is experience earned faster we focus on principles not tools
principles not models okay there's going to be an onslaught of Agents of tools of
models you know this already right you're you're aware of this we need principles to endure change over time so
you know this course helps you get there it helps you endure change with principles and one of the key principles
we talk about in lesson three is context model prompt these are the big three the
most important elements for getting work done in AI coding but really with all of generative AI there are eight lessons in
this course they take you from beginner to intermediate to advance we talk about big topics that are you know really
becoming mainstream in the generative ai ai coding world we talk about the spec prompt right scaling up your work by
writing larger prompts larger specs and we talk about you know a big topic that's come up recently is this idea of
closing the loop right by creating these closed loop self verifiable systems your
AI coding tools and your agentic systems can actually get the work done by
themselves if you give them enough direction if you tell them where to go and how to resolve and give them feedback you close the loop okay this is
a really important powerful pattern this is going to be big over 2025 and 2026 people are already starting to talk
about this more this is getting uncovered so you want to move on this stuff before it really really hits the masses okay so eight lessons here um you
know lots of great reviews feel free to check out you know tons of the other videos and AI coding content I have on
the channel um this is here for you and just to mention it I have a no questions asked refund before Lesson Four this is
basically risk-free at this point right so hop in if you don't like my style if you don't like the video if you don't
understand what's happening if it's too complex or if it's not complex enough and you're too much of an omni chat engineer and you already know what I'm
going to say in the next you know six videos or whatever that's fine you get a full refund for you start lesson 4 no
questions asked we've had zero issues with this there's a lot of value here and you know I just want to pit it on
the channel for all existing principled AI coding members I'm going to be rolling out some new tooling that helps
us use the patterns we learned in principal AI coding in a cool lightweight way I'm building this on top
of the powerful all-in-one tool UV so it's going to be super simple to set up use and deploy and we're of course going
to continue using our you know top-of-the-line uh most customizable configurable powerful AI coding
assistant AER so stay tuned for that and you know even if you don't use ader you
know even if you're not a fan of CLI based you know full control AI coding assistants that's fine um again we use
AER as a tool here to showcase the principles this course is not about AER
okay so just to quickly mention that and uh yeah that's principal AI coding uh hop in here before you know the next
wave of coding comes which I'm going to be preparing everyone for again inside
this course those lessons are in the works they're in the queue but that's going to be for later in this year just
to say it out loud here right now ai coding is the wave the next wave that's upon us is agentic coding when you fully
close the loop what you end up with is systems that can operate on their own so
stay tuned stay locked in I hope you can understand why agents are so important in the age of AI you first start with
# Why Agents Are So Important
the prompt you then move to prompt chains you have series of llm based calls that can do work on your behalf
and then you move to AI agents right this structure where you give them the tools they need to solve the problem and
then you let them learn gather information execute get feedback agents is how we continue to scale our compute
this is where we're going to be focused on the channel it's all about scaling compute usage maximizing what you can do
it's all about AI coding so that you can write faster than ever so that you can build out these agents fast you know
just to come full circle here that's why the single file agent pattern is so important because we
meet at the intersection of three important Innovations we have astrals UV
allowing us to bundle dependencies into a single file we have self- validating agent patterns where we can write great
tools and great prompts to allow the agent to self verify before it Returns
the response to us and then of course we have powerful AI coding techniques many
of these we cover in principal AI coding this lets us reuse scale clone and
duplicate our single file AI agents into many different domains you can imagine
we have an agent that builds agents okay so we have a lot of Big Ideas to cover
on the channel if you're interested in this if you made it this far in the video you know what to do drop the like drop the sub leave a comment stay
connected and whatever happens stay focused and keep building
