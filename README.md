# Tcard
Computerized T-card system, with real-time sign-in updating for command staff 

Short version: Computerized sign-in outside the trailer; real-time sign-in list gets displayed inside the trailer.

This repo has no actual code as of 11-25-16 - it's just a placeholder for ideas.

##Why?

The universal ICS T-card system is tried and tested and very robust.  It does everything we need, anyone can interpret it at a glance, and it is immune to power interruptions, network outages, and wide-area electromagnetic pulses.  Those qualities make it ideal for keeping track of your most important assets: people.

But, it does have some drawbacks:
- slow to set up
- need to keep t-cards up to date with the SAR membership list
- slow to shuffle and re-shuffle
- slow to relay (and revise) the sign-in status and team compositions from the T-card sleeve to the command staff, who are busily building team assignments and filling out assignment forms

A lot of gains could be made by computerizing the system.  Possibilities include:
- potential for real-time list on the screen inside the trailer of who is signed in (and all of their T-card info)
- teams can now be formed by command staff inside the trailer - no need to run back and forth between T-card sleeve and Operations
- names could be automatically filled in on the assignment forms
- changes to personnell and team composition would get relayed to command staff more quickly and accurately
- general reduction in paperwork (T-card team roster would be automatic)
- and more...

_The main sticking point is that the computerized system must be ROBUST and BOMBPROOF.  These are humans we are trying to keep track of.  Losing the data is absolutely not an option, which is why the manual T-cards are so hard to beat.  Any work on computerizing the T-card system MUST address that topic right from the start._

##Contributing##

There is not yet any code to contribute to - we are looking for ideas and discussion.

Take a look at the [Product Specification wiki page](https://github.com/ncssar/Tcard/wiki/Product-Specification) - that's where we are keeping the updated list of requirements, nice-to-haves, and ideas.  Due to the magnitude and gravity of this project, even though it's open-source, we need to adopt a customer/contractor workflow, with frequent design reviews and ongoing discussion between project lead(s) and developers.

Feel free to contribute by creating an Issue, adding to the Wiki, or contacting the project lead(s) directly.  Thanks in advance for your input.

**HOWEVER:** Note that there is an extremely high bar for the decision to start using any computerized T-card system, as spelled out above. In other words, the project lead is a control freak, largely out of necessity, but at least partially due to personality... Developers should stay in close contact with the project lead(s) regarding implementation plans, thoughts about what platform(s) to use, etc, before investing much time in any direction: important points about these decisions probably haven't been thought of before and won't come to light until the developer brings them up with the project lead(s).

Separately, the project lead is not the one to ultimately decide whether this system will work for the entire SAR team.  The actual 'customer' in this scenario is the SAR leadership and the incident command team as a whole, which will bring many more considerations in to play.  The project lead is on the incident command team and can try to predict many of the team's requirements, but, does not have the final say.


So far we have an Excel spreadsheet for the sign-in process; just type in the SAR member# - the name is found in a lookup table and must be verified - then they are automatically signed in at the current time.  The spreadsheet has no macros, just formulas (some being order-dependent) so it can work in the Excel app on a smartphone.  The event sign-in sheet gets imported to a separate Excel spreadsheet with macros, which keeps track of all volunteer hours for all events, but cannot run in the Excel app so it has to be stored as a file online, downloaded, updated (via import), and posted back online.
