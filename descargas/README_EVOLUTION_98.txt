GRAND PRIX WORLD - EVOLUTION '98, VERSION 0.1 (pre-release)
===========================================================

A small pack for Grand Prix World (MicroProse) that you extract over a CLEAN installation of the original game. It brings a rebuilt gpw.exe plus the texts, audio,
graphics and circuit-map files that go with it. The aim is to keep the GPW experience and fix what was broken. The only thing added on top of that is the Safety Car.

This is version 0.1, not a finished release. Most of the new features have been checked on a test bench, and the main ones have been through real races, but expect rough
edges. This file explains how to install it and, further down, what changed: for each change, what the original game did and what this pack does now.
It gives no numbers for the game's internal mechanics (probabilities, times, weights), because they are still being tuned and will change between versions. It does give the
figures for everything you can see or look up: screens, the speed selector, the 1998 season data, wages, ratings and texts.


CONTENTS
  1. What you need
  2. How to install
  3. Running it
  4. What is in the pack
  5. What changed: was / now
  6. Things you should know
  7. Reporting bugs and credits


1. WHAT YOU NEED
  - A clean installation of the original game (the retail CD or its image). You do NOT need the 1.01 or 1.03 patches: this pack replaces english.txt and gpw.exe.
  - Your own way of running GPW on a modern system (see "Running it").


2. HOW TO INSTALL
  1. Install the original game into a new folder. Do not reuse an install that already has other mods.
  2. Extract this pack INTO that folder and accept every overwrite. The folders inside the pack mirror the game's, so it creates no new top-level folders.
  3. Start gpw.exe (or the launcher you normally use).
  4. Start a NEW career. Saved games from other versions are not guaranteed to work with this one.

  To go back to the original, delete the folder and install the game again. The pack never touches anything outside the game folder.


3. RUNNING IT
  GPW does not run well on modern Windows by itself. Use whatever you prefer:
  - DxWnd (windowed). It is not included: download it yourself from https://sourceforge.net/projects/dxwnd/files/ (take the latest build, at the time of writing v2.06.16). The pack
    brings a ready-made profile, GPW_Evolution_98.dxw: import it in DxWnd, then right-click the entry, choose Modify and set the path to your gpw.exe. The path must not contain
    blank spaces.
  - dgVoodoo2, as a DirectDraw wrapper.
  - Full screen with no wrapper, if your system allows it (you may not see the race view).
  Two tips:
  - If the mouse pointer does not land where you click under a wrapper: right-click gpw.exe, Properties, Compatibility, Change high DPI settings, and tick "Override high DPI
    scaling behaviour" with "Application".
  - If the game freezes on the loading screen, try setting gpw.exe to Windows 98 / Me compatibility.


4. WHAT IS IN THE PACK
  - gpw.exe: the rebuilt executable (the 1998 variant).
  - english.txt and the text folder (COMME.TXT): the news variants, new events, injury texts, Race Control messages and the 1998 names. Only the English texts are included.
  - speeche: seven new Race Control audio files (two-hour limit, Safety Car, investigation), plus other voice clips.
  - bmp, car, textbl, tga and track: the 1998 graphics from Simul810's 1998 mod, with Ferrim's own adjustments to some textures and two driver portraits.
  - Tracks0 to Tracksf: the 16 circuit maps, with the pit lane drawn and the cars' circles redistributed to move more evenly.
  - manifiesto.csv: every file in the pack with its SHA-256, to check you have an intact copy.
  - GPW_Evolution_98.dxw: the DxWnd profile.
  - README_EVOLUTION_98.txt (this file) and CREDITS.txt.


5. WHAT CHANGED: WAS / NOW
   (Short names such as "SC" are used for the Safety Car.)

THE SAFETY CAR

   1. Safety Car
    Was:  It did not exist. A car stopped on the track changed nothing for the rest of the field.
    Now:  When a car stops on the track after an accident, a mistake, a mechanical failure or a stall on the grid, the Safety Car may come out. How likely depends on the reason.
          It can come out from the first lap, but not near the end of the race, and it is always called off with enough laps left to race again. A ghost car leaves the pit
          lane, the field slows down and bunches up behind it, and nobody overtakes except stopped or retired cars (this applies to you as well). The race restarts when it
          comes in.

   2. Fuel, tyres and parts under the Safety Car
    Was:  Consumption and wear were always the same.
    Now:  They drop while the Safety Car is out, as they would in a real neutralisation.

   3. What the AI does about it
    Was:  The AI had no logic for it and followed its pit plan.
    Now:  It re-plans: it refuels at once if it cannot reach the end, it comes in if its stop was due soon anyway, it takes a "free" stop when the cars behind are far enough away,
          and it changes tyres that are worn.

   4. Safety Car on the map
    Was:  The map showed only the cars.
    Now:  The ghost car is drawn as a silver-grey circle marked "SC", and while it waits it parks in the pit lane, a little way back from where the lane meets the track.

   5. Safety Car news
    Was:  None.
    Now:  After the race, news about the teams whose strategy was shaped by the Safety Car (a stop for lack of fuel, a last stop brought forward, a stop saved), in several wordings.

   6. Stalling on the grid
    Was:  It never happened at Monaco, Hungary or Belgium.
    Now:  It can happen at every circuit.

CAR PACE

   7. Parts, fuel supplier and driving aids
    Was:  They barely moved the lap time.
    Now:  They weigh a lot more, so a better engine, gearbox or chassis is something you can point at when a car is fast.

   8. Drivers
    Was:  A driver's Speed and Skill were close to a rounding error. Skill nudged the car by a fixed percentage.
    Now:  Speed and Skill count clearly, and Skill helps a weaker car more than a strong one. The old percentage adjustment is switched off.

   9. Pushing
    Was:  A push lap gave a small bonus and cost little.
    Now:  The bonus is much bigger and so are the costs: the risk of an error when you push, the wear on the engine and on the tyres, and the heat in the tyres.

  10. Tyre stiffness and set-up
    Was:  Stiffness and the set-up points had a small effect.
    Now:  Both weigh much more, centred on the starting set-up so the starting level does not change.

  11. Wet weather
    Was:  Rain was a bigger factor than the whole car: the driver's wet-weather skill and the car's rain set-up decided the race.
    Now:  Both are much weaker. A good wet driver still helps, but rain no longer takes over the race.

  12. Germany
    Was:  The value that sets how far apart a good car and a bad car are in speed was far from the other circuits' at Germany, so the field was squeezed together.
    Now:  It is in line with the other circuits.

AI STRATEGY

  13. Starting tyre
    Was:  Every AI car started on the hard compound, and the AI's soft tyre did not load its own grip and temperature, so it was really a hard tyre with another name.
    Now:  Some AI cars start on the soft, drawn per car once per weekend and remembered between qualifying and the race. The AI's soft tyre loads its own attributes, like yours.

  14. Number of stops
    Was:  Drawn without looking at the tyre. A soft-tyre car could end up on a single stop.
    Now:  It follows the compound: soft cars stop more and never make a single stop; hard cars can go long. Monaco has its own pattern, so the whole field does not pit together.

  15. Length of the stints
    Was:  No limit on a soft-tyre stint, and hard-tyre cars could not stay out much longer than anyone.
    Now:  A soft-tyre stint is capped to part of the distance, hard-tyre cars can stay out longer before their first stop, and no stint of an AI car is shorter than a fixed share
          of the race distance (first, in between and last). Your cars are left exactly as you set them, and team-mates never plan to stop on the same lap.

  16. Fuel
    Was:  At every stop the AI added a whole stint on top of what was left, and every car left the grid with the same amount of fuel whatever its plan.
    Now:  It adds only what it is missing, counted with the leader's laps, and each car leaves the grid with fuel for its first stint.

  17. When the weather changes
    Was:  The AI decided with fixed lap thresholds (wrong for any race that was not the usual length) and counted the laps to go with its own laps.
    Now:  The thresholds scale to the real race distance, a lapped car decides like the leader, and the first stop after a re-plan can no longer land too early and be skipped.

  18. A stop that was getting lost
    Was:  When a car was due to stop while its team-mate was in the pits, it was supposed to wait a lap, but the code compared wrongly and the stop vanished. The car also skipped a
          stretch of track while it decided.
    Now:  The stop is postponed properly and the car stays where it was.

  19. Broken front wing
    Was:  The AI carried on with it.
    Now:  If the wing is badly damaged and there are enough laps left, the car comes in to repair it, with a limited number of attempts.

  20. Qualifying runs
    Was:  A rotating pointer and a coin toss. Only one car could leave the pits at a time, and there was a limit on cars on track.
    Now:  Each car makes several runs. The first and last are scheduled by how good the car is (slow cars go out early), the others are left to chance, and there is no limit on cars
          on track. The AI stays in the pits if the track gets wetter than when the best time was set, unless it is the final stretch.

  21. Constructors' table
    Was:  Teams with no points all received the same stored position, which fed the share prices and the news with wrong values.
    Now:  Each team gets its own.

THE PIT LANE

  22. Pit stop bug
    Was:  Cars in the pit lane were ordered by a common key and each waited for the one before it in the list. A car that entered first could leave after one that entered later.
    Now:  Cars no longer wait for each other, when entering or when leaving.

  23. Speed in the pit lane
    Was:  Cars ran at the pace of the track.
    Now:  There is a speed factor in the pit lane, set per circuit, so the time lost in a stop is closer to the real one.

  24. Cars in the pit lane, on the map
    Was:  A car disappeared from the race map the moment it entered the pit lane.
    Now:  Every circuit has its pit lane drawn with its sections and points, and the cars are visible all the way through the stop.

FAILURES, WEAR AND PIT STOPS

  25. Wear and race distance
    Was:  Tyre wear and part wear per lap did not depend on how long the race was, so a short race wore far less than a long one.
    Now:  Wear is scaled by the race distance, so any race wears a car as much as a full-length one.

  26. Mechanical failures
    Was:  Only the game's random failures, with a cap on retirements per circuit.
    Now:  The cap is gone, and at a few moments of the race the game checks whether too few cars have retired and, if so, may give a healthy car a failure. The human player gets the
          same extra failure risk in the first laps as the AI.

  27. Two-hour limit
    Was:  A car finished when its own clock reached the limit, without crossing the line, and the order followed the physical order on track.
    Now:  The race ends when the leader crosses the line after the limit.

  28. Pit stop times
    Was:  The best and worst stop statistic raised any time to a minimum, and a floor on stop time wiped out the differences between tyre tables.
    Now:  The real time is recorded, and the floor only applies to a stop with no refuelling, no tyres and no repair.

PENALTIES

  29. Race penalties (false start, pit lane speeding, blue and yellow flags)
    Was:  Applied on the spot, with no investigation.
    Now:  They are held back for a few laps with an investigation notice, then applied as a stop-go or as time added to the result. If the decision comes too late to serve a stop-go,
          it becomes a time penalty. The AI comes in a few laps after the decision.

  30. Classification
    Was:  Cars on the same lap were ordered by race time alone.
    Now:  Race time plus the penalty time. The time on screen does not change.

  31. Speeding in the pit lane
    Was:  Ignored near the end of the race.
    Now:  Enforced for the whole race.

  32. Manager announcements
    Was:  The manager announced penalties during the race.
    Now:  Switched off, since the investigation notice does that job.

  33. Illegal driving aids
    Was:  The AI teams were found out with illegal aids so often that drivers kept being excluded and the championship suffered.
    Now:  The AI is found out a good deal less often. Your team is checked as before, and the limits per check and per season stay.

THE RACE

  34. Ties in position
    Was:  Cars with identical section, gap and fraction were ordered by car number.
    Now:  They keep their previous race position.

MARKET, CONTRACTS AND SIGNINGS

  35. Wages of the AI
    Was:  The AI did not limit wages by its income beyond the game's flags. Big teams ended up with a pay driver only if the best refused.
    Now:  The AI only signs drivers whose pay fits its income, with a pay-driver mode and without pay drivers at rich teams.

  36. Drivers without a seat
    Was:  A driver nobody could afford stayed free for ever, and free agents' wages only went up.
    Now:  Drivers without a seat lower their demands before each round of signings.

  37. Season close
    Was:  One round of signings.
    Now:  Several rounds.

  38. Contracts when a game is created
    Was:  Every contract lasted a year and everything expired at once at the first close.
    Now:  Contract lengths are staggered by group (drivers, test drivers, department chiefs, sponsors and suppliers).

  39. Ties between candidates
    Was:  Resolved by list order.
    Now:  The one who earns less goes first.

  40. Mid-season termination
    Was:  No team sacked a driver during the season.
    Now:  After some races a free star driver can sign for a team whose driver is performing clearly worse than the team's position; that driver is released, with news about it.

  41. FIA decision after qualifying
    Was:  The FIA admitted slow drivers who had a problem if they belonged to a top team, and also the test drivers, on top of a random quota.
    Now:  Only the random quota remains, and the last car always stays out.

  42. Starting skills of some drivers
    Was:  The 1.03 starting skills.
    Now:  Adjusted to better reflect 1998 for the drivers below (starting rating before -> now):
          Villeneuve (Williams): Skill 3 -> 4
          Irvine (Ferrari): Speed 4 -> 3, Skill 3 -> 2, Overtaking 4 -> 2, Concentration 3 -> 2
          Fisichella (Benetton): Speed 3 -> 4, Skill 3 -> 4, Overtaking 2 -> 4, Concentration 2 -> 4
          Hill (Jordan): Speed 4 -> 3, Skill 3 -> 4, Overtaking 2 -> 3, WetWeather 5 -> 4, Concentration 4 -> 3, Stamina 5 -> 4
          Panis (Prost): Speed 2 -> 3, Skill 4 -> 3, Overtaking 2 -> 3, Concentration 3 -> 4, Experience 3 -> 4
          Trulli (Prost): Speed 1 -> 4, Skill 2 -> 3, Overtaking 2 -> 3, Concentration 2 -> 3
          Diniz (Arrows): Overtaking 1 -> 2, WetWeather 3 -> 2, Experience 3 -> 2, Stamina 3 -> 2
          Salo (Arrows): Speed 2 -> 3, Skill 1 -> 3, Overtaking 1 -> 3
          Barrichello (Stewart): Speed 3 -> 4, Skill 3 -> 4, Overtaking 3 -> 4, WetWeather 2 -> 4
          Takagi (Tyrrell): Speed 1 -> 3, Skill 1 -> 2, Overtaking 1 -> 2
          Nakano (Minardi): Speed 1 -> 2, Overtaking 1 -> 2, WetWeather 3 -> 2
          Tuero (Minardi): Speed 1 -> 3, Skill 1 -> 2, Overtaking 1 -> 2, WetWeather 1 -> 2, Concentration 1 -> 2, Experience 2 -> 1
          Test drivers:
            Montoya (Williams): Speed 1 -> 4, Skill 1 -> 2, Overtaking 1 -> 2, WetWeather 1 -> 2
            Badoer (Ferrari): Speed, Skill, Overtaking, WetWeather and Concentration 1 -> 2
            Zonta (McLaren): Speed, Skill, Overtaking and Concentration 1 -> 2
            Sarrazin (Prost): Speed 1 -> 3, Skill 1 -> 3, Overtaking 1 -> 3, WetWeather 1 -> 2, Concentration 1 -> 3
            Collard (Arrows): Speed, Skill, Overtaking, WetWeather, Concentration, Experience and Stamina 1 -> 2
            Montermini (Tyrrell): Experience 1 -> 3

NEWS AND TEXTS

  43. Wordings
    Was:  Every event had a single fixed wording.
    Now:  Many events have several wordings, picked at random, with the matching headline. The pack adds 1,356 new texts in english.txt (news variants, events, Safety Car,
          penalties, the two-hour limit and strategy news).

  44. Injuries
    Was:  The news and the mail did not say how long the injury would last.
    Now:  They do, in number of races.

  45. Lost sponsor deals
    Was:  Losing a deal with a cash sponsor sent the wrong mail.
    Now:  Sponsors that are not suppliers get the "Lost Sponsor Deal" mail the game already had.

  46. Department chiefs' transfer rumours
    Was:  Some came out with the names crossed, the wrong job's text, or no news at all for the Chief Mechanic.
    Now:  Fixed.

  47. The winner's news
    Was:  The margins over the runner-up were compared the wrong way round, so the "crushed", "dominated" and "narrowly" headlines could never appear.
    Now:  They are reachable, and "won narrowly" appears for every team and only for a really small margin.

  48. 1998 names
    Was:  Sponsor, driver and team names of the original season.
    Now:  45 texts of the original are rewritten for 1998: sponsors, drivers and teams (for example "Buzzin Hornets" becomes "Benson and Hedges", "Marrano" becomes "Marlboro"
          and "John Newhouse" becomes "Jacques Villeneuve"), the injury texts and the "GAME OVER" text, which now reads "SIMPLY LOVELY".

SCREENS AND SPEED

  49. Faster races
    Was:  One simulation step per drawn frame, and a speed selector that went from 50% to 150% of real time, one point per key press.
    Now:  Several steps per frame. The selector goes from 100% to 600%, starts at 400% and moves 25 points per key press (F9 up, F8 down).

  50. Qualifying Times panel
    Was:  Long names and no laps column.
    Now:  Surnames (with an initial only when two drivers share one), and a new Laps column.

  51. Race Order panel
    Was:  It listed only the cars that had crossed the line on the current lap.
    Now:  It always lists the whole field in the live order, over two pages of eleven cars, with the stops made, the tyre fitted (D dry, I intermediate in green, W wet in red), the gap to the leader and
          the gap to the car ahead. The gap to the car ahead gives "+N L" only if the car is really that many laps behind the one in front.

  52. Pit Stops panel
    Was:  Number of stops and the fastest and slowest one.
    Now:  Every driver who has stopped, in the live race order, with three blocks, Pit 1, Pit 2 and Pit 3: the lap of each of the first three stops (L before the number, for
          example L22) and its duration in seconds, rounded to the tenth (for example 27.6s).

  53. Lap Times panel
    Was:  It only showed your own cars.
    Now:  Page Up, Page Down and the page arrows on screen take it to any driver, in race order.

  54. Windows
    Was:  Every session opened the default layout, with the TV feed and camera.
    Now:  The default layout is the map, the Race Order or Qualifying Times, Circuit Conditions and Speech Transcription. The layout is remembered between sessions.

  55. Race map
    Was:  The circles moved in jerks: instant on some straights, crawling on other sections.
    Now:  The circles move at a pace that follows how long the cars take on each stretch. This only affects the drawing, not the cars.

BUG FIXES

  56. Sound handles
    Was:  The sound code opened system events for every sound and never closed them, so in a long race thousands stayed open.
    Now:  The two places found are fixed. The growth is much smaller but not entirely gone (see below).

  57. Loading a saved game
    Was:  The game forgot how many set-up points the team had used: the buttons to lower points were disabled and the weekly process sent a stern mail and took morale away.
    Now:  The count is rebuilt on loading.

DATA TABLES AND THE 1998 SEASON

  58. Performance curve of chassis and engine
    Was:  Steep and uneven.
    Now:  The REMASTERED curve, smoother, with the same extremes.

  59. Engines
    Was:  The 1.03 starting values: each of the eight engines added up to 42 points across its seven attributes (consumption, heat, power, reliability, response, stiffness and
          weight).
    Now:  New starting values, more spread out. The totals are now Hart 28, Ferrari 38, Ford 32, Mercedes Benz 40, and 34, 30, 34 and 36 for the other four engines.

  60. Headquarters
    Was:  Staff capacity per level of 160, 200, 240, 320 and 400, and a cost per level of 1.6 M, 3.2 M, 4.8 M, 6.4 M and 8 M.
    Now:  Capacity of 120, 160, 200, 240 and 280, and a cost per level of 3.2 M, 6.4 M, 9.6 M, 12.8 M and 16 M.

  61. Non-F1 drivers
    Was:  Wages from 20,000 to 35,000, no bonuses, almost every skill at 1, and ages and nationalities from another line-up (for example Wilson: wage 26,000, Speed 1, Skill 1,
          age 30).
    Now:  Wages from 1 M to 5 M (De la Rosa and Gene are pay drivers, paying 6 M and 4 M), race and championship bonuses, skills from 2 to 4, and 1998 ages and nationalities
          (Wilson: wage 1 M, Speed 2, Skill 3, age 23). WetWeather of De la Rosa, Gene, Junqueira and Rodriguez is 2 and Verstappen's is 3.

  62. Circuits
    Was:  The 1.01 and 1.03 values (identical to each other).
    Now:  Overtaking is one point lower at Australia (5 to 4), Argentina (3 to 2), Spain (3 to 2), Canada (4 to 3), France (5 to 4), Germany (6 to 5), Hungary (2 to 1),
          Belgium (4 to 3), Italy (6 to 5), Luxembourg (5 to 4) and Japan (4 to 3), and four lower at San Marino (6 to 2). The starting rain set-up is one point higher at
          Australia, Brazil, Argentina, San Marino, Spain, Monaco, France, Great Britain, Austria, Belgium, Italy and Luxembourg, and four higher at Japan (3 to 7). France has 72
          laps (was 71) and Japan 53 (was 51).
          These values come from the REMASTERED base (Ferrim's own build, never released: the 1.03 patched with GPWEdit) and could already be set with GPWEdit; the pack keeps them as they are.

  63. Sponsors and suppliers
    Was:  The 1.03 starting ratings and classes.
    Now:  The same 98 sponsors and the same starting split between teams, with ten values changed in nine of them. Ratings: Benson and Hedges 2 to 3, Gauloises 3 to 2, Red Bull 1
          to 2, Winfield 5 to 4, and the engines Mugen-Honda and Peugeot 4 to 3. Classes: Bridgestone 4 to 5, Goodyear 5 to 4, and the engines Ford 5 to 4 and Peugeot 3 to 2.

  64. Department chiefs
    Was:  The 1.03 wages and bonuses, for example Commercial Manager 150,000, Chief Designer 250,000, Technical Director 500,000 and Chief Mechanic 150,000.
    Now:  Wages rise for 43 of the 44 chiefs (and fall for one): Commercial Manager 600,000, Chief Designer 2,000,000, Technical Director 5,000,000 and Chief Mechanic 500,000.
          Both bonuses rise for most chiefs, and the skill level of eleven chiefs and the age of eight also change.

  65. Test drivers
    Was:  Benetton, Jordan and Stewart had the test driver slot but empty: no age, wage or skills, listed as "Driver Unknown".
    Now:  They have an age, a wage and every skill at 1 (they still appear as "Driver Unknown"). These values come from the REMASTERED base (Ferrim's own build, never released: the 1.03 patched with GPWEdit) and could already be set with GPWEdit.


6. THINGS YOU SHOULD KNOW
  - Most of the new features have been checked on a test bench but not yet in many real races. The ones least seen in a race are the mid-season termination, the market changes, the new
    qualifying runs, the penalty process, the new failure checks, the pit lane speed on circuits that were not calibrated, and the new screens.
  - The sound code leaks Windows event handles in long sessions. The fix is included, but the number of open handles still grows, so very long sessions can lose the commentary sounds
    or slow down. Saving and restarting the game clears it.
  - A few circuits still use a general value for the pit lane speed. The times the AI uses to decide whether a stop is free under the Safety Car are estimates. The French and German
    versions of the new texts are not included, because they are not up to date: those languages keep the original game's texts. Some 1998 numbers are Ferrim's best reading of the real season.
  - The internal values of the game (probabilities, times, weights) can change between versions of this pack. Do not rely on numbers copied from an older version.


7. REPORTING BUGS AND CREDITS
  Any bug or annoyance you have found over the years is welcome. Post it in the GPM Planet forum or on the Discord, with the circuit, the round and what you were doing.
  You can also propose ideas and see what is already on the list at https://fermanpre.github.io/gpw-evolution-98/. Other ways to reach Ferrim are in CREDITS.txt.
  Credits and licences are in CREDITS.txt (please read it: the new audio is licensed for non-commercial use only).
