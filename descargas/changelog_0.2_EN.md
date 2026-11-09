# GPW Evolution '98 changelog: changes since 0.1 (work in progress)

**This is the living changelog.** Release 0.1 (30/10/2026) is frozen as an immutable record in `docs/historico/release_0.1_30-10-2026/` (the ES and EN changelogs, the master list, the README and the CREDITS, with their SHA-256 hashes in `SHA256SUMS.txt`; checked with `herramientas/verificar_historico.py`). Nothing here modifies that record: a mistake in 0.1 is noted in this file, not there.

**Starting point:** the published zip `GPW_Evolution_98_v0.1.zip` (SHA-256 `a431a88f…caca3a`) and its EXE `gpw_REMASTERED_neumaticos_IA_prueba17_k4_1998.exe` (SHA-256 `d884319f…768d37`).

**How it is kept.** One entry per change, with the date, what 0.1 did, what happens now and its status: *Test* (only in a test EXE or file, not the default), *Tested* (seen in a race) or *Accepted* (will go into the pack). The generator's defaults do not change until an entry becomes *Accepted*, except bug fixes, which go in by default with a `--sin-…` option to remove them (stated in the entry). Marks: [L] read in code or data, [I] inferred, [?] not determined.

Spanish version: `docs/changelog_0.2_ES.md`. The two files always carry the same entries.

---

## 31/10/2026

### 1. Safety Car: gap between cars and restart gap halved (Test)

- **0.1:** under the Safety Car, a follower more than 2 s behind the car in front runs at ×0.80 and, at 2 s or less, at the leader's pace (×0.60); the field compacts to about 2 s between cars (`--sc-hueco 2`). During the braking on the last lap the field compacts to 1.2 s (`--sc-hueco-tira 1.2`). The Safety Car is deployed with a probability that depends on the reason for the stop (18.2% accident or collision, 9.1% driver error, 3.0% mechanical failure, 25% stall on the grid).
- **Test:** a 1 s gap (`--sc-hueco 1`), a 0.6 s restart gap (`--sc-hueco-tira 0.6`) and a 100% probability on every retirement (`--sc-probabilidad 100`), to see how a tighter field behaves with many Safety Cars.
- **Status:** *Test*. It is not the default and it is not in the 0.1 zip. Test EXE: `gpw_REMASTERED_neumaticos_IA_prueba17_k4_SC100_hueco1_tira06_1998.exe` (all three changes at once). On its first run the game crashed at the start of the race (exception `0xC0000005` at an address outside every module, `0xAD35CE35`) [L: Windows event log]; I do not know whether it repeats or which of the three changes causes it [?].
- **Second run (31/10/2026, game with Tyrrell):** no incidents; the crash has not repeated [L: Ferrim]. It was the same EXE: the recorders, which wait for that process name, attached to that game [L]. The first crash is recorded as not reproduced.
- **Isolating the fault (prepared):** three EXEs with a single change each: `…_k4_A_SC100_1998.exe` (probability only), `…_k4_B_hueco1_1998.exe` (gap only) and `…_k4_C_tira06_1998.exe` (restart gap only).
- **Known risk [I]:** with a very tight field the queue may bunch up and the race order may fall back to car-number order, as happened on 22/10/2026 with ×0.80 and no gap limit. It would show in the Race Order at the restart.

### 2. Audio: Takagi's and Rosset's voice files swapped (Test)

- **0.1:** the original game's `speeche` voice files, untouched: `TAK*.wav` says "Takagi" and `ROS*.wav` says "Rossett" [L: transcribed with Whisper].
- **Now:** the contents of the five pairs (`OUT`, `P1`, `P2`, `P3`, `PIT`) are exchanged, so `TAKOUT.wav`, `TAKP1.wav`, `TAKP2.wav`, `TAKP3.wav` and `TAKPIT.wav` carry Rosset's voice and the `ROS*.wav` files Takagi's. The `ROSA*.wav` files (de la Rosa) are not touched.
- **Reason:** the game said "Takagi" where it should say "Rosset", and vice versa [L: Ferrim, 31/10/2026]. I have not checked the cause in the code [?]; it still has to be confirmed in a race that each car now says the right name after the swap.
- **Status:** *Test*. Done only in `C:\Juegos\GPW1998Mod\speeche`; the originals are in `C:\Trabajo_Claude\Evolution_98\respaldo_audio_takagi_rosset\`. These ten files were not in the 0.1 zip, so if the entry becomes *Accepted* they will go into the pack.

### 3. Safety Car: 1.5 s gap and 0.9 s restart gap (Test)

- **Observation by Ferrim (31/10/2026):** with the 1 s and 0.6 s test, playing with Tyrrell, their lapped drivers let cars pass behind the Safety Car. Cause not analysed [?].
- **Test:** intermediate values `--sc-hueco 1.5` and `--sc-hueco-tira 0.9` (with `--sc-probabilidad 100`, as in the previous test). EXE: `gpw_REMASTERED_neumaticos_IA_prueba17_k4_SC100_hueco15_tira09_1998.exe` (DxWnd profile 12).
- **Status:** *Test*. The default is still 2 s and 1.2 s. If it still happens, the values are adjusted again. A fact from the code [L]: the gap set with `--sc-hueco` is also the time distance at which the Safety Car's ghost car is placed ahead of the leader when it is repositioned (see entry 4).

### 4. Safety Car: the ghost car "teleports" backwards at the end (Observed, no change)

- **Observation by Ferrim (31/10/2026):** when the Safety Car is about to come in, it pulls away from the leader (who slows to ×0.30). Several times they have seen it "teleport" backwards to a short distance ahead of the leader, then carry on and enter the pits normally.
- **When it does not happen [L]:** not when the ghost comes out onto the track: there it runs at the rest pace (×0.10, `--sc-fantasma-reposo`) until the leader reaches it, and the repositioning only runs once it has been picked up (`alcanzado` non-zero).
- **Cause [L]:** in `fantasma_paso` (`herramientas/cuevas_safety_car.py`, label `gp_otra`) the ghost is checked against the leader's section: if, advancing at most 3 sections from the leader's, it does not reach the ghost's section, the code puts the ghost back in the leader's section with its entry clock minus the gap (`--sc-hueco`). That is, when it ends up more than 3 sections ahead of the leader, it jumps back to `hueco` seconds in front of the leader.
- **Why it happens [I]:** when the leader brakes to ×0.30 on the last lap, the ghost keeps going and exceeds the 3-section lead. I have not measured it with a recording.
- **Options:** widen the 3-section limit, make the ghost brake with the leader in that phase (closer to the cause, not applied), or leave it as it is.
- **Test (31/10/2026):** the limit is widened to 5 sections. New generator option `--sc-fantasma-secciones N` (1 to 20; default 3, as in 0.1) and a new datum in the ghost area (`DESP_SECCIONES_FANTASMA`, +0x1EC) replacing the fixed 3 in `gp_otra`. Test EXE: `gpw_REMASTERED_neumaticos_IA_prueba17_k4_SC100_hueco15_tira09_sec5_1998.exe` (DxWnd profile 13; it also carries 1.5 s, 0.9 s and the 100%).
- **Check [L]:** `probar_safety_car.py` in the emulator, 166 tests with no failures on a default EXE and on one with limit 5; the new ones (25y to 25z5) check that with 3 a ghost 4 sections ahead is put back, and with 5 it is left alone until it passes 5.
- **Status:** *Test*. The default is still 3. It has not been seen in a race yet whether with 5 the jump disappears or is only delayed: the ghost keeps its pace while the leader brakes to ×0.30, so it may still jump, further away [I].

### 5. Safety Car: pace of a car coming back from the pits (Analysis, no change)

- **Question from Ferrim (31/10/2026):** which ratio a car uses when it comes back onto the track after a free pit stop under the Safety Car.
- **Answer [L, code]:** inside the pit lane only the circuit's pit-lane limiter factor is applied (`LIMITADOR_CARRIL`: it jumps to `sin_fase` and never reaches the Safety Car part). On the track the normal follower rule applies: with a bigger gap than `--sc-hueco` to the car in front in race order it runs at ×0.80 and catches up; at that gap or less, at ×0.60. Until the leader picks up the ghost, all followers run at ×0.80 without looking at the gap. There is no special case for cars leaving the pits.
- **Data from the 31/10 game [L]:** `datos/cash_prueba_SC100_hueco1_tira06_repeticion/`: 22 pit passes, with an average pit-lane ratio of 0.65 to 0.68 and 31 to 45 game seconds. Almost all are under green (laps 13 to 28, about 97 s each); the only one possibly under the Safety Car is Nakano's on lap 1. So that game cannot measure the exit pace under the Safety Car [I]. Measuring it would need a recorder that reads every few milliseconds the ratio (+0x34) and the section of each car while the Safety Car is active.
- **Status:** *Analysis*. No code change.

### 6. Repair of wear and damage: mechanical staff's units (Test, proposal 24)

- **0.1:** the repair screen works out how much wear (`FUN_005FDB15`) and how much damage (`FUN_005FDB96`) are repaired with the **commercial department's** time units: both functions call `FUN_0056403e(team, un_XpValueH_2)` and `un_XpValueH_2` (0x015FFA18) is the value `FUN_005649D4` returns for the chief commercial [L]. Community proposal 24 pointed it out.
- **Now:** both functions use `un_XpValueH_5` (0x015FFA24), the chief mechanic's [L: the same `FUN_005649D4` ties it to the chief mechanic's person type]. One operand byte changes in each function (0x005FDB3B and 0x005FDBBC, from 0x18 to 0x24). New option `--sin-reparar-mecanicos` to go back to the 0.1 behaviour.
- **Not checked [?]:** whether the mechanical department was the original intention (it is the natural reading from the name of the screen, not a proof), how much the balance changes (each team has different units per department) and whether another part of the game repairs with the commercial units. The other calls to `FUN_0056403e` with the commercial type (sponsorship, hospitality) belong to other calculations and were not touched [L].
- **Check [L]:** the EXE generated with and without the option differs in exactly those two bytes; the anti-drift check (`changelog_inventario.py comprobar`) is clean. It has not been seen in the game yet.
- **Status:** *Test*. EXE: `gpw_REMASTERED_neumaticos_IA_prueba17_k4_REPARAR_MECANICOS_1998.exe` (DxWnd profile 14). Unlike the Safety Car tests, this EXE carries only this change (with the SC and everything else as in 0.1).
- **Note on reproducing 0.1:** with `--sin-reparar-mecanicos` the generator produces an EXE functionally equal to the 0.1 one but not byte-identical: the `--sc-fantasma-secciones` option (entry 4) replaces a fixed 3 with a memory datum holding 3. The published EXE does not change.

### 7. Version 0.2 candidate and variant with the Safety Car at 100% (Test)

- **What it is:** the consolidated EXE of everything above, without the 100%, and separately the same version with the 100%. It is not a release: there is no zip and nothing has been published.
- **Candidate** (`gpw_REMASTERED_neumaticos_IA_v02_candidata_1998.exe`, SHA-256 `4080c798…65bf1` since 02/11/2026 (with entries 24 to 30 and with Car Internals built in; without the `--sin-car-internals` option); before that `f4b0be70…2a88f` (without Car Internals), `70bc67f6…87f65` (with entry 24) and `214f3be9…fc6a8`, in `C:\Juegos\GPW1998Mod\previas_instaladas`; before that `a749b56e…72e00`, in `prueba_SC\v02_previas_11`; before that `38f0bd53…07a97`, in `v02_previas_10`; before that `47c0dd89…6575a`, in `v02_previas_9`; before that `eed83841…14ba3`, in `v02_previas_8`; before that `f5281365…f1554`, in `v02_previas_7`; before that `2f83ac72…cc229`, in `v02_previas_6`; before that `988496b5…e6d52`, in `v02_previas_5`; DxWnd profile 15): recipe `aplicar_parches_prueba10.py --k 4 --sc-hueco 1.5 --sc-hueco-tira 0.9 --sc-fantasma-secciones 5 --sc-seguidores 0.9 --sc-fantasma-lento 0.4 --sc-seguidores-lento 0.9 --salidas-hueco 3 --salidas-107 --bonus-ritmo 500 --bonus-ritmo-tope 30 --bonus-ritmo-circuito 3 --overtaking-solo-atacante --fia-tope-motores 10 --fia-tope-combustible 4 --fia-tope-neumaticos 32 --fia-ajuste-sin-cambio 1 --fia-ajuste-cambio 1` (the last fourteen options date from 01/11/2026: entries 10, 13, 16, 19, 20 and 23; entries 21 and 22, the set-up reserve cap and the pole track state, are on by default) and then `aplicar_no_f1_1998.py`. It includes: repair with the mechanical staff (entry 6), slower SC ghost while the leader brakes and ×0.90 in the catch-up (entry 10), no blue-flag penalty under the SC (entry 11), the pay-driver flag of the starters and of De la Rosa and Gené (entries 12 and 14), SC gap of 1.5 s, restart gap of 0.9 s and ghost limit of 5 sections (entries 1, 3 and 4), salary cap for chiefs with a final pass (entry 8) and no fixed test-driver veto (entry 9); the fixes of 6, 8 and 9 are on by default in the generator. The SC probability stays as in 0.1. Regenerated on 31/10/2026 with 8 and 9 (the previous version, `7e673813…`, is in `prueba_SC\v02_previas`).
- **SC at 100%** (`gpw_REMASTERED_neumaticos_IA_v02_SC100_1998.exe`, SHA-256 `0e506a83…c9e5a` since 02/11/2026 (with entries 24 to 30 and with Car Internals built in); before that `d0ad096c…8ee98` (without Car Internals), `4768d7ae…86d95` (with entry 24) and `aa7268c2…68869`, in `previas_instaladas`; before that `8dae14f5…eba02`, also in `v02_previas_11`; before that `2b8a7989…9ee0`, in `v02_previas_10`; before that `be74eee7…d1a19`, in `v02_previas_9`; before that `11c5cfca…5a8ea`, in `v02_previas_8`; before that `accdf483…557e0`, in `v02_previas_7`; before them `e165afd9…a6123`, in `v02_previas_6`; before that `667c3150…1860e`, in `v02_previas_5`; profile 16): the candidate plus `--sc-probabilidad 100`. It differs from it in 34 bytes, the SC probabilities [L].
- **Outside the EXE:** the swap of Takagi's and Rosset's voices (entry 2) is in `C:\Juegos\GPW1998Mod\speeche`, not in the EXE; a package would have to include those ten files.
- **Untested:** neither EXE has been played yet. The candidate's SC values (1.5 s, 0.9 s and 5 sections) are those of today's tests, not confirmed in a race [?].
- **Status:** *Test*.

### 8. Income-based salary cap also for department chiefs, and a final pass (Test, proposals 14 and 2)

- **0.1:** the income-based salary cap (`FILTRO_FICHAJE`) applies only to driver signings. For department chiefs the AI only checks the game's flags: Money (a probability by budget tier and Ability; with Ability 5 it is 0% below 26 M, 30% from 26 to 50 M and 60% from 51 to 70 M), Salary (the asked salary is the current one plus a percentage; it rejects nothing), bonuses and length [L].
- **Now:** `FILTRO_JEFES` hooks the entry of `FUN_0056ECB7`, the function that decides whether a chief accepts, called by in-season signings and the two end-of-season passes. It compares the salary the chief asks for with the same income-based cap as for drivers (`10% × (income/15 M)^0.825`, maximum 40%) and, if exceeded, rejects and clears the salary flag so it is rolled again. It never acts on the player's team [L].
- **Final pass:** `CIERRE_JEFES` replaces the call of `uf_XpPostSeasonFunctionUnknown` to `FUN_004CED47` (filling chief vacancies at the end of the season) with two: the normal one, with the cap, and another without a cap (level 2) for teams still missing a chief. `FUN_004CED47` only fills vacancies, so the second does not touch those already signed [L].
- **What changes in practice [I]:** a chief asking more than the cap (Newey, about 5 M, against about 1.6 M for Minardi) no longer signs for Minardi or Tyrrell by the normal route. According to the 20/10/2026 chiefs study, with the drivers' curve no starting titular exceeds his team's cap, even with the maximum 45% raise (the tightest is Tyrrell, at 0.80 of its cap), so it should not push out any current chief. It still has to be confirmed that Newey at Minardi was due to this: Minardi's estimated budget and Newey's Ability have not been measured [?].
- **Where it does not act:** the player's team; level 2 (final pass); asked salaries of 0; and for drivers the usual filter remains.
- **Option:** `--sin-filtro-jefes` removes both pieces. On by default in the generator.
- **Check [L]:** `probar_mercado.py` in the emulator, no failures; the new tests check that Minardi rejects a 5.0 M chief and accepts a 1.5 M one, that McLaren accepts the 5.0 M one, that it does nothing with the salary flag at 0, with the player's team, at level 2 or with out-of-range arguments, and that the closing calls `FUN_004CED47` twice with level 0 and level 2. The anti-drift check is clean. It has not been seen in the game yet.
- **Risks [I]:** the final pass without a cap can put an expensive chief back in a poor team if no cheap one passes the flags; the filter also affects the renewal of AI teams' chiefs (same function); what happens with the salary of academy chiefs has not been looked at.
- **Status:** *Test*. The two EXEs of the provisional 0.2 (`…_v02_candidata_1998.exe` and `…_v02_SC100_1998.exe`) carry this change since 31/10/2026 (regenerated before running Australia in the Tyrrell test game).

### 9. The original game's fixed test-driver veto is removed (Test, proposal 3)

- **0.1:** when choosing a test driver, the game discards three people by index: 14, 30 and 31, who at the start are Michael Schumacher (Ferrari driver 1), Mika Häkkinen and David Coulthard (McLaren drivers) [L]. It is a fixed list in the original game, the same in 1.01 and 1.03, not a decision of this project. It is in four places: in-season signing, the two closing passes and an injured driver's replacement, with three comparisons each [L]. It protects no other driver and does not follow the three if they change position.
- **Now:** `VETO_PROBADOR` changes the immediate of the twelve comparisons (0x1E, 0x0E and 0x1F) to -1, which no person has: in practice the veto disappears. Twelve bytes, at 0x004CB035, 0x004CB057, 0x004CB079, 0x004CDBC5, 0x004CDBCF, 0x004CDBD9, 0x004CE434, 0x004CE43E, 0x004CE448, 0x004DAA3D, 0x004DAA47 and 0x004DAA51. Option `--con-veto-probador` restores it. On by default in the generator.
- **Nothing is added in its place** (Ferrim's decision, 31/10/2026): no level filter for test drivers. With this, any driver, including the previous three, can end up as a test driver; what still holds back is the other filters: pay drivers, the income-based salary cap and the acceptance flags [L].
- **Check [L]:** the generated EXE differs from the base in exactly those twelve bytes inside the four signing functions; the anti-drift check is clean. It has not been seen in the game.
- **Expected effect [I]:** more free stars will end up as test drivers at teams that can afford them. For proposal 3 (Irvine at Sauber) nothing changes by itself; the test-driver level filter is still pending.
- **Status:** *Test*. The two EXEs of the provisional 0.2 carry this change since 31/10/2026.


### 10. Safety Car: the ghost brakes with the leader (×0.40) and the catch-up goes up to ×0.90 (Test)

- **Ferrim's observation (01/11/2026):** the Safety Car "teleports" backwards again with the 5-section limit, and the queue does not form in time: several cars stay half a lap behind.
- **Cause of the jump [L]:** the ghost runs on a fixed clock scale (pace ×0.60) while the leader, in the last-lap braking, runs at ×0.30; the ghost pulls away from the leader until it exceeds the section limit and the code puts it back behind.
- **Now:** new option `--sc-fantasma-lento F` (0.05 to 1.5; without it, the SC pace, as in 0.1): in the leader's braking phase the ghost switches its clock scale to that pace, keeping its progress inside the section (the section clock is recomputed in the same way as when the ghost is picked up). When the leader returns to its pace (normal phase), it goes back to the SC scale. Candidate value: ×0.40 (the leader drops to ×0.30; the ghost, to ×0.40). The ghost pulls away from the leader at 0.10 of pace instead of 0.30, three times slower. New datum in the ghost area (+0x4C, 256 / pace) and eleven new instructions in `fantasma_paso` (`herramientas/cuevas_safety_car.py`).
- **Catch-up:** the candidate uses `--sc-seguidores 0.9` (before ×0.80): followers farther from the car ahead than `--sc-hueco` run at ×0.90 until they close up. Those already inside the gap keep ×0.60, like the leader.
- **The leader's braking does not affect the far followers:** new option `--sc-seguidores-lento F` (0.05 to 1.5; without it, `--sc-seguidores` × `--sc-factor-lento` / `--sc-factor`, which with the 0.1 values is ×0.40 and with ×0.90 would be ×0.45). The candidate uses `--sc-seguidores-lento 0.9`: the far ones keep ×0.90 while the leader brakes to ×0.30. Those inside the restart gap keep ×0.30, like the leader. What changes is datum +0x28 of the ghost area [L]. Risk [I]: a far follower closes in at ×0.90 against a leader at ×0.30 and the pace is only recomputed when changing section, so it may end up somewhat closer than 1.2 s before slowing; it cannot overtake (`SC_ADELANTAR`).
- **Check [L]:** `probar_safety_car.py` in the emulator, 176 tests without failures (new 25za to 25zj: default slow scale equal to the SC one, scale change in the slow phase, clock kept and return to the normal scale).
- **What I do not know [?]:** whether at ×0.40 the jump disappears completely (the ghost keeps separating at 0.10 during the braking stretch) or whether ×0.90 forms the queue in time. Risk of ×0.90 [I]: more bunching; overtaking is still blocked by `SC_ADELANTAR`, but on 22/10/2026, with ×0.80 and no gap limit, the race order went back to car-number order. It will show in the Race Order.
- **Status:** *Test*. The generator defaults do not change (`--sc-fantasma-lento` absent, `--sc-seguidores` 0.80).

### 11. Safety Car: no blue-flag penalty while it lasts (Test)

- **Ferrim's observation (01/11/2026):** Villeneuve, lapped, between Schumacher and Häkkinen behind the SC, got an investigation for ignoring blue flags with the Safety Car on track.
- **Cause [L]:** the routine that counts steps with a car with more laps right behind a lapped one (`decomp_00430000.c:6050-6058`) and the "Ignored Blue Flag" roll (`FUN_0045F5B8`) do not look at the Safety Car. Under the SC the pack is compacted, `SC_ADELANTAR` prevents overtaking and the lapped car cannot move aside; the counter reaches 30 and the roll can come up.
- **Now:** `SC_BANDERA_AZUL` (0x0045F5B8, 6 bytes): with the SC active the function returns 0 without rolling. Outside the SC, as before. Option `--sin-sc-bandera-azul` removes it. On by default in the generator.
- **Not covered [?]:** letting lapped cars unlap themselves under the SC, as in real life; the game does not do it and it has not been touched.
- **Check [L]:** emulator (25za and 25zb): without the SC it follows the original path; with the SC it returns 0.
- **Status:** *Test*.

### 12. Pay drivers: the team was paying instead of being paid (Test)

- **Ferrim's observation (01/11/2026), after Australia:** his pay drivers "were being paid instead of paying", even though the game still shows their salary in red. Ferrim suspected a bug in Veedub's GPWEdit 1.1 (not checked [?]).
- **What marks a pay driver [L]:** a flag (`un_XpPersonAttributePayDriverSalaryNextYearUnknown`, +0xC68, the amount as a positive number) and a level (+0xC6C, 1 to 5). A negative salary alone is not enough: with the flag at 0, `FUN_004D10F9` (`decomp_004D0000.c:300-310`) treats the driver as a normal one and books `−salary / 16` every race in category 0xD, and `fin_PostTransaction` (`0x0055F9BA`) flips the sign of every positive amount in categories above 0xC (`decomp_00550000.c:3652-3654`). What should be income ends up as an expense of the same size. Also, `FUN_004BD12A` (the pay driver's yearly income) is 0 without the flag, so the team neither collects nor counts that money in its budget.
- **What is in the data [L]:** the 1.03 has the flag and level filled in for the five starting pay drivers (e.g. Rosset: 4,300,000 and level 2). REMASTERED, and therefore 0.1, leaves them at 0 for all 33 drivers. In Ferrim's Tyrrell game, flag 0 and level 0 were read from memory for Rosset and Takagi, with salaries of −2 M and −3 M. The defect is in the data, not in the game's code.
- **Now:** `INDICADOR_PAGO` writes the flag (the salary amount as a positive number) and the level of every starter with a negative salary, and `INDICADOR_PAGO_NOF1` (hook at `0x004706CD`, just before the last call of `FUN_0046EEBE`, the routine that creates the non-F1 drivers) does the same for De la Rosa (person 131) and Gené (person 135), who start with a pay-driver salary. Option `--sin-indicador-pago` removes both. On by default in the generator. **Salaries are not touched** (Ferrim's decision, 01/11/2026: they stay as in 0.1). The level comes from the amounts table of `uf_XpCalcPayDriverSalaryNextYear` (level 1: 2.6 to 3.5 M; 2: 3.6 to 4.5; 3: 5.6 to 6.5; 4: 7.6 to 8.5; 5: 9.6 to 10.5) [L the table, I the choice of level]:

| Driver | Team | Salary (as in 0.1) | Flag | Level |
|---|---|---|---|---|
| Pedro Diniz | Arrows | −8.0 M | 8,000,000 | 4 |
| Ricardo Rosset | Tyrrell | −2.0 M | 2,000,000 | 1 |
| Toranosuke Takagi | Tyrrell | −3.0 M | 3,000,000 | 1 |
| Shinji Nakano | Minardi | −3.0 M | 3,000,000 | 1 |
| Esteban Tuero | Minardi | −4.0 M | 4,000,000 | 2 |
| Pedro de la Rosa | free (non-F1) | −6.0 M | 6,000,000 | 3 |
| Marc Gené | free (non-F1) | −4.0 M | 4,000,000 | 2 |

- **Test drivers** are not touched. With the two non-F1 drivers marked as pay drivers and free, `FUN_004D0E76` (conversion of a free driver into a pay driver) does nothing while there is one among the free ones [L].
- **Withdrawn change:** for a few hours on 01/11/2026 this entry also restored the 1.03 salaries (Diniz −9.6 M, Rosset −4.3 M, Takagi −6.4 M, Nakano −2.9 M and Tuero −3.7 M); Ferrim asked to go back to the 0.1 ones.
- **New games only.** A saved game carries its own data: Ferrim's Tyrrell game still has flag 0.
- **Check [L]:** the generator prints the ten changes of the five starters; the disassembly of the `INDICADOR_PAGO_NOF1` cave writes to 0x011DF650/54 and 0x011E2E30/34 (flag and level of persons 131 and 135) and returns to `0x004706D2` after the original call. Not seen in the game.
- **Status:** *Test*.

### 13. Qualifying: staggered AI exits and cars outside the 107 % (Test)

- **Ferrim's observation (01/11/2026):** when it started to rain the AI left the pits en masse; Fisichella, after a bad lap (1:55.505, 125.3 % of pole), went back to the pits and stayed there although the track was not wet yet, at risk of not running again.
- **What our `SALIDAS_QUALI` cave does (test 10) [L]:** it replaces the choice made by `FUN_00451F77`. With imminent rain (time target ≥ 3 and the track still dry) every car with no time (best lap 0) goes out at once, in car-number order; in the last stretch (fewer than 6 reference laps to the end) all the pending ones go out in the same way; and while the track is wetter than when the pole was set nobody goes out. A car with a time, however bad, follows its normal plan: four exits at most, the 2nd and 3rd at random (1/3 per call), and the game's 12-lap cap.
- **Now, with two new options (off by default):**
  - `--salidas-hueco S` (0 to 30 s): at least S game seconds (18.78 ticks per second of the session clock) pass between one exit and the next, and the walk through the candidates starts at a random car, so block exits go out one at a time and in random order. The candidate uses 3 s (56 ticks). The cave's data area grows by 0x10 bytes (clock of the last exit and walk counter).
  - `--salidas-107`: a car whose time is above the pole × 107 % goes out as soon as the cursor reaches it, without waiting for its scheduled time, while the track is not wetter than when the pole was set and up to the game's 12-lap cap (so "a car outside the 107 % that goes out and does not improve keeps going out"); and it also goes out in the imminent-rain exit, not only the cars with no time.
- **What does not change:** the player's cars are not touched; cars inside the 107 % follow their plan; the block for a wetter track and the last stretch stay as they were.
- **Check [L]:** `probar_salidas_hueco.py` (new, emulator, 12 tests H1 to H12: one car per call, order set by the random number, 55 ticks are not enough and 56 are, the player's cars are skipped, the 20 AI cars all go out without repeating, outside/inside the 107 %, wetter track, 12-lap cap) and `probar_salidas_clasificacion.py` (the usual 13, with an EXE without the options) without failures. Not seen in the game.
- **I do not know [?]:** what exact rain triggers the mass exit Ferrim mentions: the cave explains it by imminent rain (target ≥ 3 with a dry track) and by the last stretch, not by anything else. With 3 s between exits, 20 cars take about 60 game seconds to go out.
- **Status:** *Test*. The new EXEs are in `prueba_SC` but **have not been installed** in `C:\Juegos\GPW1998Mod`: Ferrim carries on with the previous EXEs (candidate `ac3464f3…c4f3f`, SC at 100 % `297f9ade…ba8b2`).

### 14. Race Order on lap 0: the grid order (Test)

- **Ferrim's observation (01/11/2026):** as soon as the race screen appears, the "Race Order" panel (lap 0 of 58) showed an apparently random order: Trulli, Magnussen, Nakano, Tuero, Diniz, Panis, Salo, Takagi, Fisichella, Wurz, Villeneuve…
- **Cause [L]:** the panel reads the order list at `0x00732264` (22 entries of 28 bytes), and only the simulation loop (`FUN_0043F935`, around line 5510 of `decomp_00430000.c`) fills it, when the race starts running. Before that it keeps what was left from the previous session. Ferrim's memory read, with the race on lap 0, gave that same list (cars 11, 17, 20, 21, 14, 10…), which does not match the grid (Häkkinen, Coulthard…). The game does have the grid in place: `uf_XpInitRaceStruct1` (`0x00455B20`) stores each car's start slot at +0x44 (`decomp_00450000.c:2551-2563`).
- **Now:** `ORDEN_PARRILLA` (hook at `0x00457423`, the call to `FUN_00457432` that ends that initialisation) checks that the 22 slots exist among the cars (0 to 21; failing that, 1 to 22) and then writes into position p of the list the car that holds slot p. If slots are missing (for example, a race with no grid), it touches nothing. Option `--sin-orden-parrilla`. On by default in the generator. It is presentation only: the race does not change, because the simulation loop recalculates it as soon as it runs.
- **Check [L]:** `probar_orden_parrilla.py` (emulator, 7 tests: full grid, any permutation, no grid, repeated slot, base 1) without failures; anti-drift check clean. Not seen in the game [?]: I do not know whether in a real game the +0x44 field is already filled in when the hook runs; if it were not, the cave does nothing and the panel stays as before.
- **Fix after Brazil (01/11/2026) [L]:** in the Brazil game the panel kept the car-number order. Reading the game's memory, the start slot (`+0x44`) was filled in, but five cars (Trulli, Salo, Magnussen, Nakano and Tuero, those not amnestied from the 107 %) shared slot 21, and 17 to 20 were missing. The first version required the 22 slots to be distinct and, when they were not, did nothing. Now the cave orders by slot and, for equal slots, by car number, and only does nothing if all 22 slots are equal. `probar_orden_parrilla.py` now has 9 tests (test 6 changes from "left alone" to "ordered by slot and number" and the Brazil case with its real grid is added); without failures.
- **Status:** *Test*. It is in the new EXEs in `prueba_SC`, not in the installed ones.

### 15. Pit lane: own factors for Australia (1.00) and Brazil (0.58) (Test)

- **Ferrim's observation (01/11/2026):** in the previous race in Australia too much time was lost in every stop (Häkkinen and Hill, about 35 s).
- **Measurement [L]:** with `herramientas/calcular_factor_carril.py` and the 43 pit lane passes of that race (internal clock, general factor 0.70): a median of **39.0 s** of game time (31.3 to 42.8), with an estimated stationary time of 6.2 s (median of 16 refuelled laps, `T1` = 5 and `T2` = 36), against **28.2 s** real (113 F1.com stops from 1997 to 2001, entry to exit with the stop included). Without separating the stop it gives 0.97; subtracting it, 1.04; midpoint **1.00**.
- **Now:** Australia (circuit 0) gets its own factor, **1.00**, in the per-circuit table (`FACTORES_CARRIL_CIRCUITO` in `cuevas_safety_car.py`): the pit lane runs at track pace, with no limiter. With that value the game transit comes out at about 29 s (the natural transit of about 23 s plus the 6.2 s stationary), one second from the real 28.2 s [I: calculation with the model "time in the lane = transit / factor + stationary time"]. The other circuits do not change; option `--sc-boxes-factores` overrides it.
- **Brazil, 0.58 (01/11/2026) [I]:** in the Brazil race the AI went through the pit lane in about 30 s (general factor 0.70) against a real median of **35.5 s** (125 F1.com stops from 1997 to 2001, entry to exit with the stop included; quartiles 32.4 to 38.5 s; by year 30.9, 36.2, 33.4, 36.6 and 38.2 s). With the model "transit = natural / factor + stopped" (6.2 s stopped) it comes to 0.57 to 0.59: Brazil (circuit 1) now has its own factor, **0.58**, in `FACTORES_CARRIL_CIRCUITO`. It is an estimate from the figure of about 30 s that Ferrim gave, without the record of pit-lane passes; to be checked in the next Brazil race with `calcular_factor_carril.py`. Test 23k2e checks that Brazil carries 0.58 and the tests with an "uncalibrated" circuit now use France (7).
- **Limits [?]:** a single race; the logger loses a few seconds at the entry of the first car to enter with the lane empty, which shortens some measurements (minimum 31.3 s) and, if anything, pushes the median down; the factor should be repeated at the next Australia race, like those of Monaco and Canada.
- **Check [L]:** `probar_safety_car.py` (new test 23k2d: Australia gets 1.00 and the uncalibrated circuits the general one) without failures. Not seen in the game.
- **Status:** *Test*. It is in the new EXEs in `prueba_SC`, not in the installed ones.

### 16. Overtaking: the speed bonus based on the ratio difference (Test)

- **Origin:** the proposal in our history (`docs/preguntas_pendientes_16-10-2026.md`, line 134, and the 13/10/2026 model): overtaking should depend on pace, so that a car 1 s faster passes in a few laps and one 0.3 s faster almost never does, with the base only as a modifier. And Ferrim's question (01/11/2026) about whether the "Do or Die Block" (+10 and the 80 % outright block) lets a faster attacker through.
- **0.1 [L]:** `FUN_00444863` adds, only to the car with the higher ratio, `10 × (r − T) / (1 − T)` (0 to 10 points; only if it exceeds 1), with `r` the car's ratio and `T` = 0.9245 in Australia: it depends on the absolute ratio, not on how much faster it is than the other. The block adds 10 to the defender, equal to the maximum of that bonus.
- **Now, with `--bonus-ritmo K` (0 = off, the default):** the bonus is `min(cap, truncate(K × (natural ratio of the faster − natural ratio of the slower)))`, for the faster car (to the attacker at `[ebp-0x14]`, to the defender at `[ebp-0x10]`; with equal ratios there is no bonus). `--bonus-ritmo-tope N` (30 by default). The candidate uses K = 500 and cap 30 (since 01/11/2026; before, K = 1400): the cap is reached with a ratio difference of 0.06, about 5 to 6 s per lap; in Australia 1 s per lap ≈ 0.011 of ratio ≈ 5.5 points and 0.3 s ≈ 1.6, so only a difference of about 2 s per lap beats the +10 of the block [I: my estimate with 1 performance point = 0.0007 s]. With K = 1400 the cap was reached at 1.7 s per lap: in Brazil 12 cars saturated at 30 points against Rosset and a slow Tyrrell lost ten places in three laps (Ferrim, 01/11/2026).
- **Natural ratio [L]:** after a failed attempt the game copies the defender's ratio onto the attacker (so it follows it, `0x00442921`) and does not recompute it until it changes section; with the copied ratio the difference would be 0 from the second frame. `BONUS_RITMO_COPIA` (`0x004428F9`) replaces that copy and first saves the attacker's own ratio; `BONUS_RITMO` (`0x00444BD2`) uses for each car the saved ratio if the current one is the last copied value, and the current one if the game has recomputed it. A defender that follows another car also counts with its natural ratio. New data zone of 0x100 bytes.
- **In rain [I]:** the original bonus was lost because `FUN_0045B174` lowers everyone's ratio and leaves `r` below the 0.932 threshold. The ratio difference is kept (all drop in proportion), so the new bonus keeps working in rain; what does not change are the other point terms (orders, the block's +10 and the 80 % outright block, 2 points per wet-weather star to both).
- **Check [L]:** `probar_bonus_ritmo.py` (emulator, 11 tests: 1 s and 0.3 s, slower attacker, cap, equal ratios, ratio copy and recompute, defender with a copied ratio) without failures; anti-drift check clean. Not seen in the game.
- **Status:** *Test*. It is in the new EXEs in `prueba_SC` with `--bonus-ritmo 500 --bonus-ritmo-tope 30` (before, 1400).

### 17. Test driver signing news: wording and headlines of their own (Test)

- **Ferrim's observation (01/11/2026):** a driver's signing news does not say whether he is signed as a race driver or as a test driver; better "Jarno Trulli as a Test Driver" than "Jarno Trulli (Test Driver)", with a variant of the event of its own and its own headline.
- **How many wordings there are [L]:** the normal driver (`FUN_004FC6A3`) has **7** original wordings, each with its headline (SIDs 1269 to 1282: "DRIVER SIGNED UP", "RACER ON BOARD", "DEAL SIGNED", "ON THE DOTTED LINE", "KEY DEAL", "COMING TOGETHER" and "DEAL CONFIRMED"); the game picks one with `random(7)`. With the mod's (`VARIANTES_TEXTOS`, `datos/noticias_nuevas_EN.txt`) there are **21**: the four "team, driver" ones become twelve (4 original + 8 new) and the three "driver, team" ones become nine (3 + 6). The pay driver (`FUN_004FCF9A`) has 1 original ("HAVE CASH WILL DRIVE", SIDs 1305 and 1306) and 4 with the new ones. Neither tells the role.
- **Where they come from [L]:** they are called by the AI's hiring (`decomp_004C0000.c:1305, 1340`), the end-of-season promotion or signing of a test driver (`decomp_004D0000.c:3538`) and the player's hirings (`decomp_00570000.c:396, 417, 522, 543`). Just before, the game stores the next-year role in the person: `un_Person_TypeNextYear` (`0x0116D008 + person × 0xDF8`; 6 and 7 race drivers, 8 test driver).
- **Now:** `ROL_NOTICIA` and `ROL_NOTICIA_PAGO` (hooks at `0x004FC6A3` and `0x004FCF9A`): if the role is 8, they pick at random a wording of their own for the test driver and create the news like the original (body with `sprintf`, headline, `uf_XpCreateNewsItem` with the same type, 4 or 5, and the driver's head image). If those SIDs are not in the game's text file (pointer 0 in the string table) or the role is a race seat, the original function runs. Option `--sin-rol-noticias`. On by default in the generator.
- **New texts (SIDs 8527 to 8538, under `#RESERVA` in `datos/noticias_nuevas_EN.txt`, translated in `datos/spanish/tr_11.txt`)**, body and headline consecutive: 8527/8528 "%s has signed %s as a Test Driver." / TEST DRIVER SIGNED; 8529/8530 "%s has taken on %s as a Test Driver, ready to step in when needed." / FIRST RESERVE; 8531/8532 "%s has found a role for %s as a Test Driver." / SPARE WHEEL; 8533/8534 "%s has recruited %s as a Test Driver to work on the car." / TEST RECRUIT; 8535/8536 "%s has bought a Test Driver seat with the %s team." / HAVE CASH WILL TEST; 8537/8538 "%s has paid for the chance to be a Test Driver at %s." / PAY TO TEST. The first four take (team, driver) and the two pay ones (driver, team), like the originals. Installed in the mod's `english.txt` with `anadir_noticias_nuevas_textos.py` (SIDs 8527 to 8538, 8539 lines); `french.txt` and `german.txt` do not have them and there the original news runs.
- **Check [L]:** `probar_noticia_rol.py` (emulator, 12 tests: the four wordings of the normal driver and the two of the pay driver with their argument order, headline, type, the person's image, registers and stack; race roles; missing SID) without failures; anti-drift check clean. Not seen in the game [?].
- **Status:** *Test*. It is in the new EXEs in `prueba_SC`.

### 18. FIA chassis regulations: the design starts by itself on continuity (Test)

- **Ferrim's observation (01/11/2026):** when the FIA approves the chassis regulations and they are continuist, the game adds bars (about 3 out of 10) to next year's chassis design stage; but pressing "Start New Chassis Design" loses that progress.
- **Cause [L]:** the event is `FUN_0060D8B4` (case 0) and for every player team it calls `FUN_0060DE55(type, team)`, the continuity: from a table (random type 0 to 4 by last year's constructors' position) it gives 0 to 5 bars and, if more than 0, sends the "Design Continuity" mail and adds them to the first unfinished design, both to `un_ChassisDesignStage1Progress[k]` (bars) and to the points accumulator `DAT_008cf4d8[k]`. The bars are not the real datum: every week they are recomputed as `accumulator / points per bar` (`decomp_00500000.c:3430-3450`). The button is control `0x797F` (`uf_XpCarDesignMouseEvents1`, tooltip SID 2413): it sets `DAT_008cf49c = 1` (design under way) **and sets the four accumulators to 0**, so the bars given disappear the following week.
- **Now:** `FIA_INICIO_DISENO` (hook at the call at `0x0060DB8C`): after the continuity, if the team's design had not started and it received points, it sets `DAT_008cf49c = 1`, like the button but without clearing the accumulators. The button stops being shown and the bars are kept. If it had already started, or the table gave nothing, nothing changes. Option `--sin-fia-inicio-diseno`. On by default in the generator.
- **What I do not know [?]:** how the AI starts its designs (the loop only covers player teams); and I have not seen the game with a real continuist regulation.
- **Check [L]:** `probar_fia_inicio_diseno.py` (emulator, 7 tests: it starts with points in any of the four accumulators, does not start without points or if already under way, does not touch other teams, registers and stack) without failures; anti-drift check clean.
- **Status:** *Test*. It is in the new EXEs in `prueba_SC`.

### 19. FIA regulations: lower caps for engines, fuel and tyres (Test)

- **Ferrim's observation (01/11/2026):** with the FIA caps (engines 42 to 51, fuel 8 to 12, tyres 96 to 130) the regulations almost never act, because REMASTERED attributes sum well below them (engines 28 to 40, fuel 6, tyres 64; in 1.03 they summed 42, 10 and 96).
- **Cause [L]:** the engine (`FUN_005280A5`, `FUN_00528255`), fuel (`FUN_00529EE5`, `FUN_0052A01D`) and tyre (`FUN_00525828`, `FUN_00525A18`) functions write ten caps by hand with `MOV [EBP-x], imm32`, in two copies per type (the one that issues the regulations and the one that trims at the season rollover).
- **Now:** `FIA_TOPE_MOTORES`, `FIA_TOPE_COMBUSTIBLE` and `FIA_TOPE_NEUMATICOS` subtract N from the ten values of both copies. With the requested values: engines −10 (32 to 41), fuel −4 (4 to 8) and tyres −32 (64 to 98). Options `--fia-tope-motores 10 --fia-tope-combustible 4 --fia-tope-neumaticos 32`; they do not exist without them.
- **What I do not know [?]:** how often "Downgrade" will come up in a real game; it only shows by playing several seasons.
- **Check [L]:** `probar_topes_fia.py` (disassembly of the six functions, 6 tests: expected values and differing bytes) without failures; anti-drift clean.
- **Status:** *Test*. It is in the new EXEs in `prueba_SC`.

### 20. FIA regulations: the regulations range moves the circuits' base pace (Test)

- **Ferrim's observation (01/11/2026):** revive the idea of `FUN_00537017` (dead code): with "No Change" the teams keep developing what they have, so cars should go faster (1 %, about 1 s on a 1:40 lap); with a regulation change, slower.
- **Cause [L]:** `FUN_00537017` added −50, +50, −100, +100 or 0 ms to the per-circuit time adjustment table (`0x015F70E0`) according to `DAT_008770d0[0]`, but nothing calls it. That table is saved in the game and enters (reference + adjustment − subtraction) in quick simulation, race preparation and the floor of those times; but real time comes from the speed ratio, not from it.
- **Now:** `FIA_AJUSTE_ANUAL` (hook at `0x0050B283`, right before `FUN_0050AAC6` resets the regulations): if the chassis regulations were issued, it adds to each circuit P per thousand of its base time (reference − subtraction): negative with "No Change" (range 0) and positive with any other range. It accumulates year after year, with no cap. In addition `SC_RITMO` multiplies each car's ratio by base / (base + adjustment) of the current circuit, so a real-time lap lasts base + adjustment. With adjustment 0 it does nothing and it affects all cars equally. Options `--fia-ajuste-sin-cambio P` and `--fia-ajuste-cambio P` (percentage from 0 to 20); they do not exist without them.
- **What I do not know [?]:** whether the game uses the table anywhere else that I have not seen; and I have not seen the effect in a real race after a season rollover.
- **Check [L]:** `probar_ajuste_fia.py` (emulator, 12 tests: each range, accumulation, previous adjustment, no regulations issued, reference and subtraction tables untouched, ratio with adjustment 0, −1,000 ms and +1,000 ms, circuit with subtraction, isolation between circuits, registers and stack) without failures; anti-drift clean.
- **Status:** *Test*. It is in the new EXEs in `prueba_SC` with 1.0 % in both cases.

### 21. Set-up: the point reserve does not go above 10 (Test)

- **Observation by a community player (01/11/2026):** up to 20 set-up points earned in testing can be accumulated: apply the 10 points, repeat testing (another 10) and remove the 10 applied.
- **Cause [L]:** the reserve is `DAT_00878500 + team × 0xE0` (index 0), and it survives the race (it is only reset when starting a game and at the year change). Testing (`FUN_006088D5`) trims it to 10, but the "−" on the set-up screen (`FUN_00613C1B`, `0x00613CE5`) does an uncapped `INC`: apply 10 (reserve 0), testing (10) and remove 10 gave 20, and +10 per cycle. Ruled out: spending with the reserve at 0 or going above 10 on a parameter, because the screen disables those buttons (`decomp_00610000.c:723-748`).
- **Now:** `TOPE_RESERVA_REGLAJE`: after the `INC`, if the reserve goes above 10 it is set to 10; with the reserve at 10, removing a point from a car loses it. A saved game with more than 10 goes back to 10 on the next press of the "−". Option `--sin-tope-reserva-reglaje` removes it. On by default in the generator.
- **What I do not know [?]:** when the set-up screen can be opened relative to the test day; I have not reproduced the exploit in the game.
- **Check [L]:** `probar_tope_reserva.py` (emulator, 9 tests: reserves from 0 to 10, a game with 19, teams 0 and 10, other reserves untouched, registers and stack) without failures; anti-drift clean.
- **Status:** *Test*. On by default in the new EXEs in `prueba_SC`.

### 22. Qualifying: the pole's track state is stored when the time is set (Test)

- **Ferrim's observation (01/11/2026, Brazil):** qualifying started with an intermediates track, Takagi set the pole and the track went to rain right after; the AI kept going out all session regardless of the weather.
- **Cause [L]:** `SALIDAS_QUALI` (`FUN_00451F77`) stores in `SAL+0` the track state (`0x711250`) at the time of the pole and lets nobody out with the track wetter than then. But the cave only runs every 16 or 32 ticks and with a random draw, and it stored the state when it noticed the new pole, not when it was set. The qualifying weather step is by percentage of the session (`decomp_00430000.c:5604`; in the race it is per lap, `decomp_00440000.c:2216`), so if it changed in between the pole was attributed to the rain (4 against 4) and the block did not act.
- **Now:** `POLE_ESTADO` (hook at `0x00449486`, the assignment of a car's best lap in qualifying, `FUN_00448F20`): after the original instruction, if the time improves the stored pole or there is none, it stores the time and the track state of that instant right away; it repeats the cave's new-session reset in case the first time arrives before its first call. Option `--sin-pole-estado` removes it. On by default in the generator (with `SALIDAS_QUALI`).
- **What it does not cover [?]:** a lap that starts in one state and ends in another is stored with the final one; Ferrim considers changing the state twice in one lap will almost never happen, but a single change can and is attributed to the state at the instant of the time. Not seen in the game.
- **Check [L]:** `probar_pole_estado.py` (emulator, 11 tests: the original instruction, first pole, worse, better and equal time, new session, time 0, registers and stack, and the Brazil case: pole on intermediates, track to rain before the call and nobody goes out) without failures; with `--sin-pole-estado` the Brazil-case test fails (it stores 4 and car 19 goes out), as it should; anti-drift clean.
- **Status:** *Test*. On by default in the new EXEs in `prueba_SC`.

### 23. Overtaking: the circuit Overtaking counts only for the attacker and scales the pace bonus (Test)

- **Ferrim's observation (01/11/2026):** in Monaco the circuit Overtaking value (1) should make overtaking harder; we need to know where it is read.
- **Cause [L]:** the circuit Overtaking is characteristic 5 of its row (`0x00F5CDB8 + (circuit + 1) × 0x84`: Monaco and Hungary 1, Argentina, San Marino and Spain 2, Canada, Belgium and Japan 3, Australia, Brazil, France, Austria and Luxembourg 4, Germany and Italy 5). Each car takes the circuit base value plus whatever points it has (the AI carries some too) as its set-up, and `uf_RaceEngineUnknown` adds it to both the attacker base (`+0x2E0`) and the defender base (`+0x2E4`). So it cancelled in the comparison and the circuit Overtaking had no influence between AI cars.
- **Now, with two options (off by default):**
  - `--overtaking-solo-atacante`: `OVERTAKING_SOLO_ATACANTE` (`0x00536B18`) removes that term from the defender base (`MOV EAX,[EBP-0x94]` becomes `XOR EAX,EAX` and 4 `NOP`). It only counts for the attacker: 1 to 5 more points depending on the circuit.
  - `--bonus-ritmo-circuito N` (0 to 10; 0 = no scaling): `BONUS_RITMO` multiplies K and the cap by Overtaking / N, reading the circuit row from the game table (`[0x15F321C] + 1`; with no data, scale 1). With N = 3 and K = 500, cap 30: Monaco and Hungary a third (cap 10), Argentina, San Marino and Spain two thirds (cap 20), Canada, Belgium and Japan as before (cap 30), Australia, Brazil, France, Austria and Luxembourg 4/3 (cap 40) and Germany and Italy 5/3 (cap 50).
- **Careful [?]:** with N = 3 the circuits with Overtaking 4 (Brazil and Australia among them) get a bonus a third larger than with the previous candidate (K = 500 without scaling equals Overtaking 3); I have not seen how it feels in a race.
- **Check [L]:** `probar_overtaking_solo_atacante.py` (emulator, 8 tests: with the patch the defender base does not add the Overtaking, also with chassis defect 6; a control EXE without the patch does add it) and `probar_bonus_ritmo.py` (now 20 tests, with the per-circuit scale: Monaco, Argentina, Canada, Germany, scaled cap, defender and a circuit with no data) without failures; anti-drift clean.
- **Status:** *Test*. In the new EXEs in `prueba_SC` with `--bonus-ritmo-circuito 3 --overtaking-solo-atacante`.

### 24. Weather replan: the 20 % minimum stint also applies (Test)

- **Ferrim's observation (01/11/2026):** at San Marino (62 laps) the track dried around lap 38 and Häkkinen, with 24 laps to go on hard tyres, got two stops (laps 40 and 52), leaving a last stint of 10 laps. Villeneuve and Irvine, with 19 to 21 to go, were already on one stop.
- **Cause [L]:** `FUN_0045E979` decides 1, 2 or 3 stops only from the laps remaining (our `DIST40` and `DIST19`, scaled to the distance: from 20 to 40 scaled laps, a coin toss between one and two) and puts the second stop at the first plus half of what remains. `STINT_MINIMO` only acts on the initial plan: the replan does not go through it.
- **Now:** `MONACO_REPLANTEO` (`0x0045EBA6`), the same hook, checks the 20 % minimum of the distance (rounded up, (N + 4) / 5: 13 laps with 62) after the number of stops is decided. While there are two or more stops and ceil(remaining / stops) − 3 is below the minimum (the 3 is the worst first stop: `laps + 2 + draw (0 to 1)`; it was 4 with the 0 to 2 draw, see the 08/11/2026 adjustment), one stop is removed, with no coin toss and never below one. At Imola: up to 30 laps remaining, one stop; from 31 to 45, the usual coin toss; with 46 or more there can be three. The stint in progress does not count. It goes with `STINT_MINIMO`: `--sin-stint-minimo` removes it; with `--sin-monaco-paradas` the hook keeps only the minimum (`REPLANTEO_MINIMO`).
- **Adjustment of 08/11/2026 (Ferrim, France):** the `−4` was computed with `A7`'s 0 to 2 draw; entry 42 (`REPLANTEO_AGRESIVO`, 04/11/2026) made it 0 to 1, so the worst first stop is `+3`, not `+4`. `SUB EAX,4` becomes `SUB EAX,3`. With 72 laps (minimum 15) the one-or-two-stops coin now applies with 35 or more laps remaining (before, 37). `probar_monaco_paradas.py` updated to the new rule, without failures.
- **Soft cap [I]:** not applied in the replan. With soft tyres and a single stop, the stint may go over 40 % of the distance (up to about 5 laps over at Imola). Measured with the lap CSVs of the test races (144 stints of 12 or more laps, soft against hard at the same lap of the stint): loss of 0.06 s per lap at 0.3 to 0.6 wear, 0.20 s at 0.6 to 0.9, 0.31 s at 0.9 to 1.2 and 0.38 s at 1.2 to 1.5 (only 8 samples). At 0.048 wear per lap on soft (Australia), five laps over cost about 2 to 3 s, against about 28 s for a stop (Argentina). Decided by Ferrim on 01/11/2026 "at least for now".
- **Check [L]:** `probar_monaco_paradas.py` (emulator, part C: 18 tests with 45, 58, 62 and 78 laps, two and three stops, soft and Monaco; one Monaco expectation changes from 2 to 1 because of the minimum) with no failures; with `--sin-stint-minimo` part C fails as it should. Anti-drift clean. Not seen in the game [?].
- **Status:** *Test*. In by default in the new EXEs in `prueba_SC`, and since 02/11/2026 in the candidate and the SC100 installed in `C:\Juegos\GPW1998Mod` (45 emulator tests on the candidate: only `probar_safety_car.py` (14) and `probar_salidas_clasificacion.py` (7) fail, the same failures the previous one already had; `probar_monaco_paradas.py` passes with 0 failures, and the previous one failed 11 in part C, as it should).

### 25. Race screen: 'Car Internals' tab with the state of the parts (Test)

- **Ferrim's request (01/11/2026):** a screen in the race simulation with the value of each part, reusing the ten-square bars. Decided on 02/11/2026: bar = current counter / starting value × 10, bar only (no number), its own tab called 'Car Internals' (one per driver) and only the seven large-scale parts (brakes, clutch, electronics, gearbox, hydraulics, suspension and throttle).
- **Data [L]:** the counter of part k (0 to 6) is at `+0x390 + 4k` of the car record and its starting value at `+0x3C0 + 4k` (copied at the start, `decomp_00450000.c:2410-2422`). It corrects the `+0x3B0` range that had been noted.
- **Now, with four hooks (`--sin-car-internals` removes them):**
  - `CAR_INTERNALS_CICLO` (`0x004A508C`): in a race, the arrows cycle through panels 0 to 7, 0x16 (Car Internals of driver 1), 0x17 (driver 2), 8 to 11 and the replay, skipping the panels of an unavailable car as the game does. In qualifying and practice, the original cycle.
  - `CAR_INTERNALS_DESPACHO` (`0x0049EF6D`): draws seven rows with an English label and a ten-square bar, with the same redraw control as the car panel 6 and 7. The bar goes from 0 to 10, with 1 while anything is left, capped at 10 if the counter exceeds the starting value.
  - `CAR_INTERNALS_BOTONES` and `CAR_INTERNALS_TITULO` (`FUN_0048F7D5`): no buttons 8 and 9, and the title 'Car Internals: driver surname' with the driver's face.
- **Texts:** the labels and the title are fixed English strings in the data area of the new section (`0x3CC0` onwards), with no new SIDs; they are not translated with the game language [?].
- **Check [L]:** `probar_car_internals.py` (emulator, 76 tests: cycle with and without replay, car 1 or 2 unavailable, session 0, seven rows and bars, cap and minimum, redraw, buttons and title) with no failures; the other 45 tests give the same results as before (only `probar_safety_car.py` (14) and `probar_salidas_clasificacion.py` (7) fail). Anti-drift clean. Not seen in the game [?]: real position and width of the rows and the bars.
- **Status:** *Test*. built into the candidate (`4080c798…65bf1`) and the SC100 (`0e506a83…c9e5a`) on 02/11/2026. The file `gpw_REMASTERED_neumaticos_IA_v02_candidata_internals_1998.exe` in `C:\Juegos\GPW1998Mod` (DxWnd profile 17) is identical to the candidate and stays as a duplicate (before that `a2bc6c05…09eb0`, in `previas_instaladas`). Not tested in a race.

### 26. Parts: starting counters shift one reliability level (Test, proposal 19)

- **Observation (community proposal 19, analysed on 02/11/2026):** reliability rating 5 gave the same starting value as rating 4 for every part.
- **Data [L]:** the starting value of the seven part counters (`+0x3C0..+0x3D8`) comes from three tables indexed by the part's reliability rating, 0 to 5 (`decomp_00530000.c:1830-1846`): brakes and suspension (`0x015FE438`), clutch, gearbox, hydraulics and throttle (`0x015FE450`) and electronics (`0x015FE468`). In 1.03 all three repeat the last value. The aids (power brakes, automatic gears and active suspension) add 100 per level; the other parts get no aid.
- **Now:** `FIABILIDAD_CONTADORES` shifts the three tables one level, with 5 at the value it had and 0 one step lower:

| Rating | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Brakes and suspension, before | 600 | 850 | 1100 | 1350 | 1600 | 1600 |
| Brakes and suspension, now | 350 | 600 | 850 | 1100 | 1350 | 1600 |
| Clutch, gearbox, hydraulics and throttle, before | 1000 | 1300 | 1600 | 1900 | 2200 | 2200 |
| Clutch, gearbox, hydraulics and throttle, now | 700 | 1000 | 1300 | 1600 | 1900 | 2200 |
| Electronics, before | 50 | 100 | 150 | 200 | 250 | 250 |
| Electronics, now | 25 | 50 | 100 | 150 | 200 | 250 |

- **Effect:** ratings 0 to 4 start with one step less life (250, 300 or 50 depending on the part) and 5 stays as it was, now different from 4. Option `--sin-contadores-fiabilidad` goes back to the 1.03 tables. On by default in the generator.
- **What I don't know [?]:** whether the repetition of 5 was intended; nor how much the failure rate changes (the counter only opens the door to a failure when it reaches 0).
- **Status:** *Test*. In the installed candidate, SC100 and candidate with Car Internals of 02/11/2026. Details in `docs/propuesta_19_diseno_hallazgos_02-11-2026.md`.

### 27. Design department: four fixes from proposal 19 (Test)

- **Origin:** points 1, 3, 4 and 5 of community proposal 19 (point 2, the FIA one, is entry 18). Readings and figures in `docs/propuesta_19_diseno_hallazgos_02-11-2026.md`.
- **Technology progress counter [L]:** when a part was completed (buttons `0x79A9` to `0x79AF` of `uf_XpInternalTechnologyConstructionUnknown`) the game set the progress to 0 but not the accumulator (`0x008CF684 + part × 4 + team × 0x2FC`); choosing the part again made the progress 10 in the first week and added another rating point. `PROGRESO_TECNOLOGIA` (`0x005DD750`) sets the accumulator to 0 too. Cancelling already did it right. The season change still resets the progress without the accumulator [?].
- **CAD building [L]:** `FUN_0050C192` returns the building bonus by phase and level; the Design phase row (the CAD) was six zeros. `CAD_BONO` sets it to 0, 100, 200, 300, 400 and 500, like the others.
- **Phase weights [L]:** the chassis efficiency weighed the Design, CFD, Model Design and Wind Tunnel phases 4, 3, 2 and 1, and their duration is 900, 300, 400 and 600. `PESOS_FASE_DISENO` (`uf_GetChassisDesignEfficiencyRating`, `0x0050C3C4`) makes them 4, 1, 2 and 3 (sum 10, the maximum stays at 100).
- **Suspension rating 5 [L]:** table `0x015FE3A8` was 0, −15, −10, −5, 0, 0 (5 equal to 4 and 0 better than 1, 2 and 3). `SUSPENSION_RATING` makes it −20, −15, −10, −5, 0, +5. The reliability half of this mistake is entry 26.
- **Options:** `--sin-progreso-tecnologia`, `--sin-cad-bono`, `--sin-pesos-fase-diseno` and `--sin-rating-suspension`. On by default in the generator.
- **Check [L]:** `probar_diseno_propuesta19.py` (emulator, 1,323 tests with the fixes of entries 27 and 28 and 119 with the EXE without them to validate the harness): the accumulator and progress of any part and team go to 0 without touching the others, the efficiency is 4/1/2/3 for several teams and values with EBX, ESI and EDI preserved, the building bonuses by phase and level, and the tables. The anti-drift check (`changelog_inventario.py comprobar`) comes out clean.
- **What I don't know [?]:** whether the zero in the CAD row was intended; how much the AI's design efficiency changes (it uses the same functions, so it is affected too).
- **Status:** *Test*. In the installed candidate, SC100 and candidate with Car Internals of 02/11/2026.

### 28. Driving Aids: the progress accumulator is also reset when the aid is completed (Test, proposal 19)

- **Observation (proposal 19):** "the same possibly happens with Driving Aids". Checked in the code [L].
- **Cause [L]:** when an aid is completed (buttons `0x79BC` to `0x79BF` of `uf_XpDriverAidConstructionUnknown`) the game sets the progress to 0 but not the accumulator (`0x008CF700 + aid × 4 + team × 0x2FC`); only the FIA's rejection roll resets it (`decomp_00500000.c:4607`). The project cost depends on the aid and the current level (Active Suspension 400 to 800, Automatic Gears 200 to 600, Power Brakes 100 to 500, Traction Control 300 to 700).
- **Effect [I]:** after an approval, the next project started with 5 to 8 out of 10 progress (10 times the previous cost divided by the next level's cost) or, if the previous level had not been built yet, finished in the first week.
- **Now:** `PROGRESO_AYUDAS` (`0x005DED21`) also sets the accumulator to 0 when the aid is completed. Option `--sin-progreso-ayudas`. On by default in the generator.
- **What I have not touched [?]:** the cost uses the current level, not the pending one, so raising another level before building the first costs the same; left as a possible separate proposal.
- **Check [L]:** `probar_diseno_propuesta19.py` (part E): the accumulator and progress of each aid and team go to 0 without touching the others.
- **Status:** *Test*. In the installed candidate, SC100 and candidate with Car Internals of 02/11/2026.

### 29. Illegal aids: the AI risks less, and less as the season goes on (Test)

- **Ferrim's request (02/11/2026):** the AI should not be so suicidal about fitting illegal aids (entry 7 of 0.1 only cut the chance of being caught, from 52 % to 26 %).
- **Cause [L]:** `FUN_0052EE65`, at the end of every race, makes each AI driver adopt a built, unapproved aid with a fixed 10 %, without looking at the risk, which rises every round. Full reading in `docs/ayudas_ilegales_IA_27-10-2026.md`, sections 6 and 7.
- **Now:** `AYUDAS_ADOPCION_1` and `AYUDAS_ADOPCION_2` (`0x0052F018` and `0x0052F061`): the adoption becomes `P % × (16 − round) / 16` per driver and round, with P = 3 by default. Round 1: 2.8 %; round 8: 1.5 %; from round 16, none. Options `--sin-adopcion-ayudas-ia` and `--adopcion-ayudas-ia P` (0 to 10). On by default in the generator.
- **Unchanged [?]:** the window between building and approving, the AI's approval (still no roll; only the player's uses the FIA table, Ferrim's decision) and the AI copying the player's aids.
- **Estimated effect [I]:** with a simplified simulation of mine (invented detection formula), the illegal use drops to a fifth and the chance of a team ever being caught in a season goes from 58 % to 17 %.
- **Check [L]:** `probar_adopcion_ayudas_ia.py` (emulator, 504 tests with the generated EXE and expected failures with the original): thresholds for rounds 1 to 18 and both draws, the 0 or 99 returned and continuation at the next instruction.
- **Status:** *Test*. In the installed candidate, SC100 and candidate with Car Internals of 02/11/2026.

### 30. General wear: new rate table with the scaling built in (Test)

- **Observation (Acescheil, Discord, 02/11/2026):** at Hockenheim "the wear is enormous": he started with wear 13 and 21, the 13 barely finished and the 21 retired with a part failure.
- **Cause [L]:** the general counter (`+0x380`, 100 minus the car's wear) drops per lap by the value of the 16-rate table at `0x015F3058`, and 0.1 also multiplied it by 72 / laps × km / 305 (`DESGASTE_PIEZAS_1` and `2`). At Germany, Belgium and Japan (rate 1.0) the race drop went from 45, 44 and 53 in 1.03 to 72, and with the session closing the total reached 94 to 98 points; below 31 the "Part Failure" zone starts (`FUN_0044534C`).
- **Now:**
  - `TASA_DESGASTE_GENERAL` sets the rate table to 0.6, 0.8, 0.4, 0.6, 0.2, 0.4, 0.2, 0.4, 0.7, 0.3, 1.1, 0.2, 1.1, 0.6, 0.2 and 1.0 (before 0.6, 0.9, 0.4, 0.6, 0.2, 0.5, 0.2, 0.4, 0.7, 0.2, 1.0, 0.1, 1.0, 0.5, 0.1 and 1.0). Option `--sin-tasa-desgaste-general`.
  - The values have the distance scaling built in (rate × 72 / laps), so the cave no longer scales the general counter: it drops what the table says. To scale it again, `--escalar-desgaste-general`. The parts are still scaled by 72 / laps.
  - Result per race, in counter points: Germany 49.5, Belgium 48.4 and Japan 53 (in 0.1 all three were 72, and 45, 44 and 53 in 1.03); Austria 21.3, Hungary 15.4 and Luxembourg 13.4 (14.2, 7.7 and 6.7 in 1.03).
- **The closing [L]:** `FUN_004F698F` (called when each session closes, with the race number) subtracts laps × constant, with its own table of 17 floats written on the stack (immediates from `0x004F699F` to `0x004F6A08`): position 0 is 0 and the next 16 are half the 1.03 rates, except Hungary and Luxembourg, which are 0.1 and not 0.05. It does not use the table at `0x015F3058` (this corrects what I said before). `CIERRE_DESGASTE_GENERAL` makes them half of the new table: 0.3, 0.4, 0.2, 0.3, 0.1, 0.2, 0.1, 0.2, 0.35, 0.15, 0.55, 0.1, 0.55, 0.3, 0.1 and 0.5. Option `--sin-cierre-desgaste-general`.
- **Effect [I, my calculation]:** adding race and closing for the 16 circuits, 780 points against the 756 of 1.03 (856 with 0.1). After a race, Germany goes from 94.5 to 74.3 points (67.5 in 1.03), Belgium from 94.0 to 72.6 (66.0) and Japan from 98.5 to 79.5 (79.5); Austria, Hungary and Luxembourg rise to 32.0, 23.1 and 20.1 (21.3, 15.4 and 13.4 in 1.03).
- **Check [L]:** `probar_sc_mitad.py` (emulator), with a new test of the general counter's drop without scaling (and with `--con-escala` for an EXE generated with `--escalar-desgaste-general`), and `probar_cierre_desgaste_general.py` (34 tests: the drop of each of the 17 positions of the closing table and that the counter does not go below 0; with `--original` for the 1.03 constants).
- **Status:** *Test*. In the installed candidate, SC100 and candidate with Car Internals of 02/11/2026.

### 31. Rain: the AI splits tyre choices between team-mates when the water goes from 3 to 4 or from 4 to 3 (Test, proposal 28)

- **Proposal 28 (Acescheil, 02/11/2026):** "when it rains and the track has got wetter or drier, split the strategies: the driver ahead on track pits for the tyres suited to the new dampness and the other stays out as normal".
- **Cause [L]:** `FUN_0045E979` re-plans each car's stops when the fitted tyre is not the ideal one for the track water level (`DAT_00711250`, 0 to 4) and its driver's wet-weather skill (table `0x015F2FF0`: with skill 3 to 5 the ideal is intermediate at level 3 and wet at level 4), but it explicitly discards the intermediate-against-wet case; when the water goes from 3 to 4 or from 4 to 3 it does nothing. `FUN_0045E4F9` changes the level by ±1 and calls it.
- **Now, without touching the usual logic (`--sin-clima-reparto` removes it):**
  - `CLIMA_REPARTO_1` and `2` (`0x0045E56E` going up, `0x0045E73F` going down): right before that call, and only if the new level is 4 (coming from 3) or 3 (coming from 4), a pre-pass marks, in each AI team, which car pits. The number 1 (driver role 1) decides first; if neither is, the best-placed car on track. It pits with 80 % (`--clima-reparto-prob P`); if not, the team-mate is asked with another 80 %. Only an AI car that is still in the race and has an intermediate or wet tyre different from the ideal is asked; the dry tyre is still handled by the usual re-plan.
  - `CLIMA_REPARTO_3` and `4` (`0x0045EB08` and `0x0045EB26`): in the two jumps that discard the intermediate-against-wet case, a marked car goes on with the usual re-plan (first stop 1 to 3 laps later, and the usual stints) and the others are discarded as before. The marks are cleared after the call.
  - Probabilities at 80 %: both fail 4 % of the time and stay out; one pits 96 %.
- **My decisions [?]:** if the first does not need to change (already has the right tyre) it spends no roll and the team-mate is considered; the player's cars and retired cars are not asked.
- **Check [L]:** `probar_clima_reparto.py` (emulator, 24 tests: decision order, retired number 1, player's car, dry tyre, tyre already right, levels that are not 3 to 4 or 4 to 3, skill 1, clearing of the marks and the two discards).
- **Status:** *Test*. Installed on 02/11/2026 in the candidate (`941e76ad…`) and the SC100 (`9e2b0f68…`).

### 32. Final order: an applied and unserved stop-go adds 25 s (Test, proposal 31)

- **Proposal 31 (Acescheil, 02/11/2026):** "if a driver, one lap or more behind the leader, receives a penalty as time added at the end of the race, the game fails to apply it correctly".
- **Reading [L]:** the final classification (`FUN_00533F3B`, `ORDEN_PENALIZACION` since 0.1) adds the penalty seconds to the race time and so breaks ties between cars on the same lap. The new test `probar_orden_final_doblados.py` (emulator, 19 tests, with those of the unserved stop-go) checks that it works with lapped cars: +25 s to a lapped car loses him the places he had in hand (up to 25 s) against other lapped cars, and never changes the order between cars on different laps. Without our patches the final order ignores every penalty, lapped or not.
- **A gap that did exist [L]:** a stop-go already applied and not served when the flag falls added nothing (only the +25 s already added and the held penalty counted). A car lapped two or more times suffers it more, because the decision to switch to +25 s uses the race laps and not the laps it has left [I].
- **Now:** `ORDEN_PENALIZACION` also adds 25 s to a car that finishes with event code 5 to 8 still pending in `+0x140` (the game clears it when the stop ends). The time shown does not change. Option `--sin-stopgo-sin-cumplir` removes it. On by default in the generator.
- **Untouched [?]:** that the decision to turn a penalty into +25 s uses the race laps instead of the laps a lapped car has left; this change partly covers it.
- **Status:** *Test*. Installed on 02/11/2026 in the candidate (`941e76ad…`) and the SC100 (`9e2b0f68…`).

### 33. Final classification: a penalty can leave a car lapped, and the panel shows it (Test, proposal 31)

- **Rule (Fernando, 02/11/2026):** when the race ends, a car with a time penalty drops behind the cars with fewer laps that finished behind him on track within that penalty, and counts as lapped. The comparison is made at the last lap both cars completed (with the lap-time sums of `0x00712460`): if the other car was behind at that line and by no more than the penalty, the penalised car drops behind and loses a lap. With several lapped cars in reach he takes the laps of the one with the fewest.
- **Penalty that counts:** the milliseconds already added, +25 s of a held penalty and +25 s of an applied, unserved stop-go (entry 32). It only acts once the race is over (some car has the total laps), and never for retired cars.
- **Now:** `DOBLADOS_ORDEN` (in `FUN_00533F3B`, `0x00533FB6`) uses the effective laps in the order key, so the points follow that order. In the "Race Order" panel the Gap and Int columns use those laps: the demoted car shows "+N L", and its Int against the car that passed it includes the penalty (for example +2.500 with a 22.5 s lead and +25 s). A red "+Ns" appears after the name with the seconds that count (during the race the added ones; once it is over, also those of the held penalty and the unserved stop-go). Option `--sin-doblados-penalizacion` removes it. On by default in the generator.
- **Tests:** `probar_orden_final_doblados.py` (26) and `probar_clasificacion.py` (new scenario); full battery 51 tests, 0 failures.
- **Status:** *Test*. Installed on 02/11/2026 in the candidate (`941e76ad…`) and the SC100 (`9e2b0f68…`).

### 34. Pit lane: Spain lane factor from 0.58 to 0.68 (Test)

- **Ferrim's observation (02/11/2026):** in Spain the pit loss is around 35 s, more than the 1997-2001 history (median 28.9 s from entry to exit over 203 F1.com stops).
- **Now:** `FACTORES_CARRIL_CIRCUITO[4]` goes from 0.58 to 0.68 (the ratio inside the lane rises, the pass is faster). With the model loss = c + natural / factor and a natural transit of about 18 s, it removes about 5 s [I].
- **Status:** *Test*. Installed on 02/11/2026 in the SC100 (`addf37e7…`); the candidate (`17c5038c…`) was installed on 03/11/2026 together with entry 35 (SC100 `24af0a28…`). To be checked in the next Spain race with the loss measured by laps.

### 35. Player stop-go penalty: free pit calls until the lap it is served automatically (Test, proposal 32)

- **Proposal 32 (Acescheil, 02/11/2026):** with a penalty to serve in the pits, the game locks the "pit now" order, waits 3 laps and serves it.
- **Cause [L]:** it comes from our 0.1 and the game together. `ENTRADA_BOXES` makes the held penalty wait and serves it on the third lap, for the player too; and the game hides the "Pit now" button while a penalty event is pending (`+0x140` > 0, site `0x0051C751`) and resolves any entry with that event as a penalty stop, without refuelling or changing tyres (`FUN_00445C0E`, `0x00445C8E`).
- **Rule (Fernando, 03/11/2026):** the player keeps the 3-lap limit, but may call the pits freely to refuel and change tyres in the first two; it is only blocked on the third, when it is served automatically.
- **Now:** for the player's two cars, while it is not yet time to serve it (completed laps minus the application lap, the same count as `ENTRADA_BOXES`): `JUGADOR_PIT_BOTON` draws the "Pit now" button and `JUGADOR_PIT_SERVICIO` resolves the entry as a normal stop and leaves the penalty pending. When it is time to serve it, the car enters by itself and the stop is the penalty one. The AI does not change. Option `--sin-sancion-jugador-libre` removes it. On by default in the generator.
- **Tests:** `probar_sancion_jugador.py` (emulator, 16 tests: free inside the window, blocked when due, AI unchanged, outside a race).
- **Unchecked [?]:** the on-screen behaviour (button visible and click effective), which can only be seen by playing a race with a penalty.
- **Status:** *Test*.

### 36. The AI really repairs a broken wing and checks breakdowns outside the points (Test, proposal 33)

- **Proposal 33 (Acescheil, 02/11/2026):** "if the AI breaks a wing, it pits, does nothing and goes back on track, retiring soon after"; and a driver with any car problem late in the race who is falling down the order should pit to "check" it so as not to retire pointlessly, while one in the points takes the risk of staying out.
- **Cause of the wing [L]:** the pit check that restores the wing (`FUN_004479C0`) only runs if the car carries the check order (`+0x3D8` = 3), the one the player gives in the pits menu (`FUN_005310C6`, case 4). When the wing breaks the game leaves that order at 0 and the AI never sets it, so `ENTRADA_BOXES` (0.1) brought the car in but with no repair.
- **Now:** when the AI decides to come in for the broken wing (below 30, more than 3 laps to go, 2 attempts at most, in any position), the cave sets `+0x3D8` = 3 and the stop repairs it. Also `REVISION_AVERIAS`: an AI car with any other breakdown (problem code `+0x43C` not 0) comes in to check it if it runs outside the points (from 7th place of the live order on) and has more than 3 laps to go; inside the points it stays out. With three laps or fewer to go nobody comes in, even if the breakdown happened earlier. The attempts are the same 2 per car. Option `--sin-revision-averias-ia` removes only the second part; `--sin-ala-ia` removes everything. On by default in the generator.
- **Tests:** `probar_revision_averias.py` (emulator, 15 tests: broken wing inside and outside the points, three laps, attempts, breakdown in 6th and 7th place, the player, outside a race).
- **Unchecked [?]:** that the AI stop really repairs in a race (it can only be seen by playing one), and how many breakdowns are repairable: the check fails 25 % of the time by the game's design (`FUN_004479C0`).
- **Status:** *Test*. Installed on 03/11/2026 in the candidate (`35527ff9…`) and the SC100 (`2eb4fc96…`).

### 37. Initial chassis of five teams from Ferrim's handling Excel (Test)

- **Ferrim's request (03/11/2026):** put the chassis values of his table and confirm the engine power of each team.
- **Now:** `CHASIS_EQUIPOS` changes the initial handling (`un_ChassisHandlingThisYearsCurrent`, immediate `mov` in `.text`) of five teams: Ferrari 74 to 76, Benetton 64 to 62, Jordan 53 to 59, Stewart 38 to 40 and Minardi 21 to 24. McLaren 91, Williams 67, Prost 41, Sauber 49, Arrows 34 and Tyrrell 31 already matched the table. Option `--sin-chasis-equipos` removes it. On by default in the generator. It only applies to new games.
- **Engine power [L, engine table at `0x01605440` of the EXE]:** Hart 2, Ferrari 6, Ford 3, Mercedes 7, Mugen-Honda 6, Peugeot 5, Mecachrome 6, Toyota 6; they match the Engine column of the table for McLaren (Mercedes 7), Ferrari (6), Williams and Benetton (Mecachrome 6), Jordan (Mugen-Honda 6), Sauber (Ferrari 6), Prost (Peugeot 5), Stewart, Tyrrell and Minardi (Ford 3) and Arrows (Hart 2). The engine-to-team assignment is the 1998 one [I]: I did not read it from the EXE.
- **Status:** *Test*. Installed on 03/11/2026 in the candidate (`fb784c7d…`) and the SC100 (`34136d86…`).

### 38. Weather in the race advances by race time, as in qualifying (Test, proposal 27, first part)

- **Proposal 27 (anonymous, 31/10/2026):** the weather simulation in qualifying and in the race is handled differently: in qualifying it depends on session time and in the race on the leader's lap; it asks for both to depend on time, so that it cannot be predicted that the weather will change when the leader crosses the line.
- **Reading [L]:** in qualifying the game gives one weather step (`FUN_0045E4F9`) per 1 % of session time (`decomp_00430000.c:5591-5606`); in the race, when a car completes the lap marked by the counter `DAT_00701830` (`0x00449937`), that is, once per leader lap. Report: `docs/propuesta_27_clima_viento_03-11-2026.md`.
- **Now:** `CLIMA_TIEMPO`: in the race, when a car completes a lap, the clock of that crossing (`+0x470`, in milliseconds) is divided by 72,000 ms (1 % of the two-hour limit, 7,200,000 ms, Ferrim's idea) and a step is given when the quotient reaches the counter; the counter still starts at 1 and rises one at a time. With ~22 cars crossing per lap, the step falls a few seconds from the theoretical instant and no longer coincides with the leader's line. Outside the race nothing changes. The draw of the new weather target (`DAT_00710ff0`, by laps) is not touched. Options: `--sin-clima-por-tiempo` removes it and `--clima-paso-ms N` (10,000 to 600,000) changes the step. On by default in the generator.
- **Effect [I]:** a race of 85 to 100 minutes receives 70 to 83 steps, against the 58 to 78 laps before: the weather moves somewhat more (up to 20 %). To keep the old pace, raise the step (for example 85,000 ms).
- **Tests:** `probar_clima_tiempo.py` (emulator, 9 tests: exact steps, a single step per crossing, lagging cars, laps no longer rule, outside the race as before).
- **Not done:** the wind part (the setup Wind parameter rules and not the real speed) and the eight chassis problems.
- **Status:** *Test*. Installed on 03/11/2026 in the candidate (`9160b2f3…`) and the SC100 (`b94706ba…`).

### 39. The AI lowers its orders in steps as the part counter falls (Test)

- **Ferrim's observation (04/11/2026, Australia):** too many brake failures (his own, with Braking at 1, had to pit half a dozen times from lap 45). He asked to "live on the edge a bit more": the AI should start lowering orders with target 5, 4, 3, 2 and 1 as the counter falls to 800, 700, 600, 500 and 400.
- **Reading [L, `decomp_00450000.c:4005-4052`]:** in `FUN_0045B21E` (per car and lap) the AI, and only the AI (`+0x7060AC` at 0), subtracts 1 from some orders when the part counter drops below 400: brakes (`+0x7063F0`) lower Braking; suspension (`+0x706404`), KerbUse and OffRacingLine; clutch (`+0x7063F4`), Braking and Acceleration. AI orders are random at the start (`FUN_004D8072`: 1 to 10, mean 4.7, and 1 19 % of the time). With 18 to 30 counter points per lap, the 400 threshold leaves little margin.
- **Now:** `ORDENES_IA_FRENOS`, `ORDENES_IA_SUSPENSION` and `ORDENES_IA_EMBRAGUE` replace that single threshold with a ladder: with the counter below 800, 700, 600, 500 or 400, the target order is 5, 4, 3, 2 or 1, and each lap each of those orders above the target drops 1 (one at a time, as before). Orders already at or below the target are left alone. Humans do not change. Option `--sin-ordenes-ia-adaptativas` goes back to the 400 threshold.
- **Tests:** `probar_ordenes_ia.py` (emulator, 169 tests: the eleven counter steps, five order values, the three blocks, humans unchanged and the full ladder over 40 laps).
- **Not done:** reverting or softening the shift of the starting counters of entry 26 (brakes 350 to 1600), which by my calculation explains the Australia brakes; Ferrim prefers to "live on the edge" for now.
- **Status:** *Test*. Installed on 04/11/2026 in the candidate (`d8891507…`) and the SC100 (`7c367bf5…`).

### 40. The AI order ladder, also for the gearbox, hydraulics and throttle (Test)

- **Ferrim's request (04/11/2026):** apply the ladder of entry 39 to the gearbox, hydraulics and throttle, which had no rule of their own, "to see what happens".
- **Reading [L, `decomp_00450000.c:3970-4091`]:** the gearbox (`+0x7063FC`) subtracts `coefficient + KerbUse + Acceleration`, the hydraulics (`+0x706400`) `coefficient + OvertakePosition + OvertakeBackmarkers` and the throttle (`+0x706408`) `coefficient + Acceleration + TopSpeed`. With REMASTERED's engines the coefficient (`10 − Rigidity`, `10 − Heat`, `10 − Response`) is 4 to 6. The total race drop averages about 1,040 points (72 × sum, independent of the circuit). With the entry 26 table, the probability that an AI car reaches 0 and fails in Australia is 57 to 83 % with rating 0, 21 to 47 % with rating 1, 4 to 14 % with rating 2 and almost nil with 3 or more [I, random orders].
- **Now:** `ORDENES_IA_CAMBIO`, `ORDENES_IA_HIDRAULICA` and `ORDENES_IA_ACELERADOR` insert the same ladder (counter below 800, 700, 600, 500 and 400: target order 5, 4, 3, 2 and 1, dropping 1 per lap) right after each counter's subtraction (`0x0045B783`, `0x0045B7E3` and `0x0045B843`), on KerbUse and Acceleration, on OvertakePosition and OvertakeBackmarkers, and on Acceleration and TopSpeed. AI cars only. Option `--sin-ordenes-ia-cambio-hidraulica-acelerador` removes it.
- **Tests:** `probar_ordenes_ia.py` (292 tests, with the new ones: eight steps, five order pairs and humans unchanged).
- **Expected effect [I]:** fewer hydraulics failures (which never lowered its orders before) and somewhat fewer gearbox and throttle failures in cars with rating 0 to 2.
- **Status:** *Test*. Installed on 04/11/2026 in the candidate (`c2a1f761…`) and the SC100 (`8a880347…`).

### 41. The weather replan does not delay an already planned stop (Test)

- **Ferrim's observation (04/11/2026, Brazil):** Coulthard's original strategy had him pit on lap 55; with the water replan from 2 to 3 he stopped on 57. "If he has no fuel, he stops on his lap and fits the tyre he needs."
- **Cause [L, `FUN_0045E979`, `decomp_00450000.c`, and the replan log of 04/11/2026]:** in the three branches (one, two and three stops) the replan computes the new first stop as `laps + draw (0 to 2) + 1` (`+2` with `A7`), stores it in `+0x324`, clears the others and recomputes the fuel to load. It does not look at whether the car already had a nearer stop: in the log, Coulthard went from `[31, 55]` to `[57]`, two laps above the one that was due and with the fuel loaded to reach 55 [I: his tank just before was not read].
- **Now:** `REPLANTEO_SIN_RETRASO_UNA`, `_DOS` and `_TRES` (`0x0045EBD2`, `0x0045EC6E` and `0x0045ED7A`, right after `A7`): if the car has a pending stop (a plan entry `+0x324` to `+0x330` with a lap greater than or equal to the completed laps + 1, the same count `FUN_004433D1` uses) and the new first stop is later, it keeps the nearest pending one. If the new one is earlier or equal, nothing changes. The tyre fitted, the following stops and the fuel come from that first stop, as always. Option `--sin-replanteo-sin-retraso` removes it. On by default in the generator.
- **Tests:** `probar_replanteo_sin_retraso.py` (emulator, 33 tests, the three branches: Coulthard's case, pending equal, later and earlier than the replan, no plan, an entry already passed, pending in the fourth entry and several pending).
- **Not done [?]:** in Brazil three teams (McLaren, Arrows and Minardi) did not replan when the water went from 3 to 4 although their only live car was eligible; it is unexplained.
- **Status:** *Test*. Built on 04/11/2026 (candidate `5be89a9d…`, SC100 `a101ff72…`). The SC100 is installed; the candidate is in the working folder, pending copy because the game had it open.

### 42. Weather replan: the first stop comes sooner, and the split between team-mates includes cars with a breakdown in progress (Test)

- **Ferrim's request (04/11/2026):** the AI should pit 1 or 2 laps after the replan, not 2 to 4; and look into why in Brazil McLaren, Arrows and Minardi did not replan when the water went from 3 to 4.
- **Reading [L]:** the new first stop was `laps + draw (0 to 2) + 2` (the `+2` is `A7`: with `+1` the car skipped the stop). In the Brazil log it came out 2 to 4 laps above the car's lap. With `A7` the safe floor is `+2`.
- **Now:** `REPLANTEO_AGRESIVO` (`0x0045EBC5`, `0x0045EC61`, `0x0045ED6D`) changes the draw argument from 3 to 2: `laps + draw (0 to 1) + 2`, that is, `+2` or `+3`. Option `--sin-replanteo-agresivo`. On by default in the generator. Check: `probar_replanteo_agresivo.py` (the three `PUSH 2` followed by the draw call and `A7` intact).
- **Team-mate split (`CLIMA_REPARTO`) [L, correction to entry 31]:** the eligibility condition required state `+0x12C` equal to 0. That left out a car with a breakdown in progress (state 1) or in the pit lane (state 2), although it is still racing, for no reason other than my conservative reading. Now only the retired car (state 3 or more) is left out. Likely explanation for Brazil [I: unconfirmed, those cars' state was not logged]: Coulthard, Salo and Nakano had a part counter at 0 and were in state 1. `probar_clima_reparto.py` goes to 27 tests (with states 1, 2 and 3).
- **Status:** *Test*.

### 43. Weather replan: the ideal tyre does not depend on WetWeather (Test)

- **Ferrim's observation (04/11/2026, Argentina, change from 4 to 3):** the ideal for rain is always intermediate at level 3 and wet at level 4, whatever the driver's skill; the driver complaining that he needs wet tyres with the track right for intermediates does not change that it is best to leave him on intermediates. Diniz, Panis and Tuero (WetWeather 2, on wets) should have been part of the pick and were not.
- **Cause [L]:** the ideal tyre table (`0x015F2FF0`, index `WetWeather × 5 − 5 + level`) gives wets already at level 3 for WetWeather 1 and 2 and is only used by `FUN_0045E979` (the replan) and `FUN_0045EF1B` (the radio message to the player). With it, a WetWeather 2 car on wets at level 3 "already had the ideal" and was neither replanned nor offered the split; and one on intermediates (Salo, Nakano, Magnussen) looked as if it needed wets, was marked and pitted to fit intermediates again (seen with Salo on lap 21).
- **Now:** `IDEAL_SIN_WETWEATHER` (`0x0045EA03`: `MOV EAX,[EAX+0xF5E098]` becomes `MOV EAX,3` and `NOP`) makes the replan always read the WetWeather 3 row (level 3 intermediate, level 4 wet), and the eligibility of the team-mate split (`CLIMA_REPARTO`) does the same. The player's radio message is untouched: the driver still complains. Option `--sin-ideal-sin-wetweather`. On by default in the generator.
- **Tests:** `probar_clima_reparto.py` (29 tests: skill 1 on wets when dropping to 3 is marked; on intermediates, skills 1 and 2 are not) and `probar_replanteo_agresivo.py` (the bytes of the new site).
- **Status:** *Test*. Built on 04/11/2026 (candidate `119dfefb…`, SC100 `2f6480e3…`); the SC100 is installed and the candidate waits in `parches\candidata_pendiente_*.exe` until the game is closed.

### 44. The pit stop bug fix is in the builds again (Test)

- **Ferrim's observation (04/11/2026, Argentina):** in the pits, the car with the smaller number overtakes the one with the larger number, as in the pit stop bug of the early tests.
- **Cause [L, checked by reading the EXEs]:** the fix (`SINESPERA_C` and `SINESPERA_R`, `0x004423E2` and `0x004426E8`) is switched on with `--sin-espera-boxes` (the name is an activation order) and was in tests 5 to 16. From test 17 (29/10/2026), and therefore in 0.1 and in every 0.2 candidate and SC100, the flag was not passed to the generator: both sites are the game's originals. There was no decision to remove it [I]: the generation option list was carried over without the flag.
- **Check of the rest [L]:** comparing byte by byte the EXEs of tests 4 to 17, 0.1 and the earlier 0.2 builds with the new candidate, no other patched site (code or data) is missing; only those two.
- **Now:** the generation option list carries `--sin-espera-boxes` (noted in the project memory). It is still an experiment: 0 inversions in 13 pairs against 17 % in the control in tests 5 and 6, not statistically proven, and with the visual risk of a car going through a parked one.
- **Status:** *Test*.

### 45. The saved game keeps the stop times and the rest of the new section's state (Test)

- **Ferrim's observation (05/11/2026):** saving and loading a game in mid-race leaves the "Pit Stops" panel with every time at 0.0 s.
- **Cause [L]:** the game saves the session state with `FUN_00460ED1` (at the end of the save file and in `Save
ace.sav`) and reads it with `FUN_00461792`; nothing our caves put in the new section is on that list: neither the stop table, nor the time penalties and held sanctions, nor the scaled-wear remainders.
- **Now:** `GUARDADO_ESCRITOR` (`0x00461788`) and `GUARDADO_LECTOR` (`0x00462049`), the last jump of each function, append and read at the end of the file a `GP2S` block + size + a copy of five state zones (stop table, penalties and sanctions, remainders and counters). The block sits after everything the game reads, so games saved earlier load as before (with those figures at 0). Option `--sin-guardado-estado` removes it.
- **Limit [L]:** the Safety Car in progress is not saved; loading with one on track loses it.
- **Tests:** `probar_guardado_estado.py` (emulator, 14 tests: writing, restoring, old file, different size, registers preserved and neighbouring zones untouched). It found and fixed the caves clobbering ESI and EDI.
- **Status:** *Test*.

### 46. Fix: the weather re-plan did not store the stops (Test)

- **Ferrim's observation (05/11/2026, Spain):** it rained for several laps and no AI team came into the pits.
- **Cause [L]:** `REPLANTEO_SIN_RETRASO` (entry 41, `0x0045EBD2`, `0x0045EC6E` and `0x0045ED7A`) declared a 6-byte patch over 5 original bytes and overwrote the first byte of the next instruction (`LEA EAX,[EAX+EAX*8]` became `NOP`). The address where the new first stop is stored came out wrong, so the re-plan changed tyres and fuel but wrote no stop. It affected every weather re-plan since entry 41 and no test saw it, because `probar_replanteo_sin_retraso.py` runs the cave in isolation.
- **Now:** length 5 at the three sites.
- **Safeguards [L]:**
  1. The generator refuses to build if a patch's declared length differs from its original bytes or if the end of the overwritten area falls in the middle of an instruction of the original executable (disassembled with capstone). Checked: with the wrong length it aborts.
  2. Integration test `probar_replanteo_integrado.py` (emulator): runs the real re-plan routine with every patch and checks that the 20 AI cars on dry tyres get a new first stop when the water rises to 3 and to 4. The previous candidate gives 3 failures and the new one 0.
- **Status:** *Test*.

### 47. Monaco: more part wear and driver-error crashes (Test)

- **Ferrim's request (06/11/2026, Monaco):** 17 cars on track on lap 70 is too little attrition for the era; no part counter reached 0 (minimums in the last photo: brakes 106, suspension 163), and driver errors almost never end in a crash.
- **Cause [L]:** a part can only fail with its counter at 0, and the wear per lap is scaled by the real distance of the circuit (Monaco: 260 km over a 305 reference). Random breakdowns (`FUN_004486C8`, once per car and lap) give only 2 % "Accident" and 9 % "Driver".
- **Now:**
  - `--desgaste-piezas-monaco PCT` (150 by default): wear of the part counters at Monaco goes to 150 %. Parts only; tyres and the general counter do not change.
  - `CHOQUES_MONACO` (`0x00449F4D`, `--sin-choques-monaco`, `--choque-monaco N`): at the end of each lap, at Monaco and in a race, a healthy, non-retired car (AI or player) with more than 3 laps to go has a 1 in 500 chance of hitting the barriers (reason 6, breakdown in progress and a possible driver injury). With about 20 cars and 77 laps that is about 3 crashes per race. The player's cars too (Ferrim's request). The Safety Car treats it as an accident.
- **Same-day fix [L]:** the first version closed the game at the green flag: the cave is entered by a `JMP` (the generator replaces the `CALL` with `E9`), with no return address on the stack, and my cave returned with `RET`. Now it makes the `CALL` to `FUN_004486C8` itself and leaves with `JMP 0x00449F52`. The emulator test simulated a call with a return on the stack and missed it; it now reproduces the entry by `JMP`. Safeguard: the generator refuses to build if a patch site is a `CALL` and the cave does not jump to the next instruction.
- **Tests:** `probar_choques_monaco.py` (emulator, 26 tests).
- **Status:** *Test*.

### 48. The "Position" tab shows 5 drivers ahead and 5 behind (Test)

- **Ferrim's request (05/11/2026):** the "<driver>'s Position" tab of the race panel wasted space: it only showed 2 cars ahead and 2 behind.
- **Reading [L]:** `FUN_0049FE90` draws the tab and `FUN_004A05AF` fills it, with 5 rows in five fixed tables (ids, position, names, teams and margins). The window is centred on the driver with a minimum of 3rd and a maximum of 20th, and it is filled in stages (3, 4 and 5 rows) as the car crosses sections.
- **Now:** `POSICIONES_TABLAS`, `_FILAS`, `_VENTANA` and `_ETAPAS` (`--sin-posiciones-11`): the five tables move to the new section with room for 11 rows, the drawing and filling loops are 11 long, the window shows 5 cars on each side (it slides so there are always 11 with 22 cars: the leader sees positions 1 to 11 and the last car 12 to 22) and the stages become 3, 7 and 11 rows. The original tables are not touched, so the saved-game format does not change; after loading a game the tab refills at the first section the car crosses.
- **Tests:** `probar_posiciones_11.py` (emulator, 10 tests): runs the real fill routine and checks the window at 1st, 3rd, 9th, 20th and last, the 3- and 7-row stages, both players and that no reference to the original tables is left in the drawing or filling code.
- **Not seen [?]:** how it looks on screen (whether 11 rows fit well in the tab's height). Each row takes 15 pixels, 165 in total.
- **Status:** *Test*.

### 49. The AI re-plans its pit stops after an unscheduled stop and uses it to refuel and change tyres (Test)

- **Ferrim's request (05/11/2026, Spain):** Herbert came in for repairs on lap 11 (only 7.2 s) and carried on with the old plan, which did not count on that stop. "He should use it to switch to a 2-stop or even a 1-stop strategy."
- **Cause [L]:** the unscheduled-stop branch of `FUN_00445C0E` (`0x00446681`) adds field `+0x36C` to the fuel and fits the tyre in `+0x370`; for AI cars they are 0 and 9 ("none"), so the AI only repaired. Nobody rebuilt the plan (`+0x324` to `+0x330`, stop laps).
- **Now:** `REPLANTEO_AVERIA` (`0x00446681`, `--sin-replanteo-averia`): for an AI car in a race, the unscheduled stop is the first stop of the new plan. Number of stops S (counting the unscheduled one) with the weather re-plan thresholds on the remaining laps scaled to 58: up to 19, one; 20 to 40, two with soft in the dry and a coin between one and two otherwise; over 40, three with soft in the dry and a coin between two and three otherwise; no stop is added when the old plan has none pending; and no stint below 20 % of the distance. The S-1 following stops are spread evenly (current lap + remaining · m / S). Example (65 laps, unscheduled stop on lap 11, plan 16-36-50): 11-29-47 or 11-38. At the unscheduled stop the car takes the fuel needed to reach the next stop (+3 laps; +2 on the last stint, to the finish) and a fresh set of the tyre it runs (the branch then picks the compound for the water level and resets the wear); the stop takes as long as the fuel and the change need.
- **Tests:** `probar_replanteo_averia.py` (emulator, 58 tests): Ferrim's example with soft and with the coin, a single stop, a completed plan, the middle band, the 20 % minimum, water 3, the player's cars, qualifying, and that the stack and registers are left intact.
- **Not seen [?]:** in a race. The fuel unit (+0x6C) is deduced from how the original plan hands it out (one unit per lap) [I].
- **Status:** *Test*.

### 50. Sponsors: the continuing contract shows the level the team signed (Test)

- **Report by Acescheil (02/11/2026, proposal 29) and confirmation by Ferrim (06/11/2026):** on the sponsors screen, contracts of more than one year with suppliers show as "works" even when the contract is customer or partner; it happens from the very start of a new game.
- **Cause [L the reading, I the cause of the data]:** the list of continuing contracts draws the level read from `+0x3EC` of the sponsor slot (`0x8240DC` in the working copy), not the level the team signed; in a new game `FUN_004EA71E` fills that field with the slot level, and at the year change it is copied from `+0x41C`, which is also the slot's.
- **Now:** `NIVEL_CONTRATOS_1` to `_3` (`0x0064393D`, `0x006459A8` and `0x00648374`, the three copies of that screen; `--sin-nivel-contratos` removes them): the cave reads the team in the slot and the sponsor type (2 to 4) and draws the level that team has stored for next year (`0x12037A8 + type × 4 + team × 0x1E90`). With no team, another type or a level outside 1 to 3, it draws what it always did. A renewed customer contract keeps showing as customer next year, because the level belongs to the team, not the slot. Only what is drawn changes.
- **Tests:** `probar_nivel_contratos.py` (emulator, 90 tests: the three sites, each type, slot 11, sponsor 98, team 11, no-data cases and registers and stack intact).
- **Not checked [?]:** that `0x12037A8` is filled in a real new game; if it were not, the screen stays as before (no worse).
- **Status:** *Test*.

### 51. The wind penalises the setup Wind deficit (Test)

- **Ferrim's request (03 and 06/11/2026, proposal 27, second part):** that the wind affects the car in a logical way.
- **Reading [L]:** the only use of the Wind setup in the pace (`FUN_0045A143`, `0x0045A5A8`) adds `T_FE330[setup Wind]` only if `Wind < 2 × wind`. The table is `0, 0, 0, −25, −75, −150`, so the loss RISES with the setup Wind (from 3 to 5), there is no loss with 0 to 2 or with 8 to 10, and with Wind 6 or 7 a second table that is not meant for this is read. The maximum was −150, about 0.1 s per lap.
- **Now:** `VIENTO_DEFICIT` (`0x0045A5A8`, 36 bytes; `--sin-viento-deficit` removes it): the index becomes the deficit `2 × wind − Wind`, capped at 5, and the penalty is `T_FE330[deficit] × N`: nothing with a deficit of 2 or less, −25 × N with 3, −75 × N with 4 and −150 × N with 5 or more. `--viento-escala N` (0 to 10; 4 by default) multiplies it: the maximum becomes −600, about 0.4 s per lap [I, from the −150 ≈ 0.1 s equivalence]. The less Wind is set against the real wind, the more is lost.
- **Tests:** `probar_viento.py` (emulator, every wind 0 to 4 and every Wind 0 to 10, another car, registers and stack intact, leftover NOPs).
- **Not checked [?]:** the seconds-per-lap equivalence and which Wind setup the AI cars carry (if all carry 0, with wind 3 or 4 they all lose the same). To be measured in a race.
- **Status:** *Test*.

### 52. The season change resets the Technology progress accumulator (Test)

- **Pending from entry 26 (proposal 19):** resetting the Technology parts' accumulator when a part is completed was already done, but the season-change one was missing.
- **Cause [L]:** the season change (`FUN_0050AAC6`, `0x0050B1B3`) zeroes each part's effort and progress, but not the accumulator `0x8CF684 + part × 4 + team × 0x2FC`; progress is accumulator / cost, so a part with a high accumulator comes back with progress 10 when started again and grants another rating point.
- **Now:** `PROGRESO_TECNOLOGIA_TEMPORADA` (`0x0050B1B3`, 11 bytes; `--sin-progreso-tecnologia-temporada` removes it) zeroes the accumulator too.
- **Tests:** `probar_diseno_propuesta19.py` (case A2: three teams × seven parts, neighbours untouched, returns to `0x0050B1BE`); 2226 tests, 0 failures.
- **Status:** *Test*.

### 53. Tyre Grip above 5 gives performance again (Test)

- **Report by Jose21crisis (29/10/2026, proposal 20):** tyre Grip reduces errors and increases consumption and temperature, but from 6 up it adds no grip, so a Grip 5 tyre can be faster than a Grip 10 one.
- **Reading [L]:** the performance-by-Grip table (`0x015FE348`, 12 cells, read in `FUN_0045A143`) is `0, −250, −200, −150, −100, −50, 0, 0, 0, 0, 0, 0`: it rises by 50 per level up to 6 and then goes flat. The effect on consumption and temperature remains.
- **Now:** `GRIP_NEUMATICO` (data at `0x015FE348`; `--sin-grip-neumatico-alto` removes it) continues the slope: Grip 7 to 10 give +50, +100, +150 and +200 (about 0.04 s per lap per level [I, at 14 performance points per 0.010 s]). The stiffness table (`0x015FE378`) stays as it was.
- **Tests:** `probar_diseno_propuesta19.py` (case D: the Grip table and the stiffness table).
- **Status:** *Test*. The rest of proposal 20 is not done (engine reliability, preferred supplier, choice by R&D, Works teams' design, suppliers leaving and entering, Hospitality).

### 54. High morale gives less effort to the departments (Test)

- **Report by Jose21crisis (29/10/2026, proposal 18):** morale levels 4 and 5 give +10 % and +20 % department effort, which makes it very easy to keep a competitive team (more spares, faster testing and sponsor signing, and a cheaper staff). It asked to lower them to 100 % or to minimal values such as 102.5 % and 105 %.
- **Reading [L]:** `FUN_0056403e` computes the department effort and adjusts it by the morale level from `FUN_00564227` (1 to 5): −40 %, −20 %, 0, +10 % and +20 %.
- **Now:** `MORAL_ESFUERZO_4` and `MORAL_ESFUERZO_5` (`0x005641A0` and `0x005641B8`; `--sin-moral-esfuerzo` removes them) set levels 4 and 5 to +5 % and +10 % (values set by Ferrim on 07/11/2026). Levels 1 to 3 do not change, so high morale is still rewarded but no longer unbalances. It also applies to the AI, which uses the same function.
- **Tests:** `probar_moral_esfuerzo.py` (emulator, 16 tests: multipliers 5 and 10, leftover bytes as NOPs, continuations intact and levels 1 and 2 untouched).
- **Status:** *Test*. The report asked for 100 % or 102.5 and 105 %; Ferrim set 105 % and 110 % (07/11/2026).

### 55. "Live Championship Standings" panel: the drivers' and constructors' championships live, with arrows (Test, proposal 5)

- **Proposal 5 (Acescheil and others) and Ferrim's request (07/11/2026):** a new panel on the race screen with the drivers' championship in one column and the constructors' in the other, and green up and red down arrows for whoever gains or loses places.
- **Data [L]:** a driver's season points are at `0x0116C42C + person × 0xDF8` and a constructor's at `0x0120262C + team × 0x1E90`; `un_ProcessRaceResults` (`0x005B8C5D`) adds them at the end of the race with the scale 10, 6, 4, 3, 2 and 1 to the first six of the final order. The live order is `0x00732264` (28 bytes per place, the car in the first value) and a retired car has state `+0x12C` = 3.
- **Now:** a new panel type, `0x18`, in the panel arrow cycle right after "Car Internals" (it shares the four hooks with it: `CAR_INTERNALS_CICLO`, `_DESPACHO`, `_BOTONES` and `_TITULO`). It shows the championship as it would stand if the race ended now: season points plus those of the current position (retired cars not counted). Each row carries the place (by points and, if tied, by race position), the arrow, the name and the points; the player's cars and team are in yellow. It fits as many rows as the panel rectangle allows (`0x015F6EF8 + panel × 0x10`).
- **Arrows:** the place before and the place now are counted with ties at the bottom (number of drivers with equal or more points): two drivers with no points do not move even if others score, and an arrow only appears if someone is passed or passes you. They are drawn with the game's own drawing context (the same sequence as its text function) and the GDI functions of the import table (`CreatePen`, `SelectObject`, `MoveToEx`, `LineTo`): a triangle nine pixels wide and five lines high.
- **Options:** `--sin-clasificacion-viva` removes the panel; `--sin-flechas-clasificacion-viva` leaves it with text only (in case the arrows cause trouble); `--sin-car-internals` removes only the other tab. The four hooks are generated if either panel remains.
- **Tests:** `probar_clasificacion_viva.py` (emulator, 266 tests: headers, place, name and points of every row, the player's colour, arrows and the GDI protocol on a fake context, retired cars, ties, a small panel and 60 random scenarios against a separate reference model) and `probar_car_internals.py`, updated to the new cycle.
- **Not seen [?]:** in the game. The real position and width of the columns, whether the team name fits, and above all that the arrows show (the drawing context is obtained the way the game's text function does it, but it is only checked with fake objects). If anything fails, `--sin-flechas-clasificacion-viva`.
- **Limits [I]:** it only shows the 22 drivers of the race (not one who scored with another team and no longer races); it does not count time penalties applied at the end; and the race points are added at the end, so the panel would stop being valid once the results are processed (the race screen is no longer drawn then).
- **Status:** *Test*.

### 56. A car that has already crossed the line after the chequered flag keeps its result if it retires (Test)

- **Ferrim's report (08/11/2026, Canada):** Wurz was fifth and "retired" on the final lap, and Villeneuve took his place in the points. The retirement happened after Wurz had crossed the line.
- **Reading [L]:** at each finish-line crossing `FUN_00448F20` adds a lap to the car; if it has completed the total laps or reached 2 hours, it is added to the arrival list (`0x00706008`) and its failure state is cleared. The race ends when a car already in that list crosses again (the leader's extra lap; `FUN_0044A637`). Until then everyone keeps running, and a lapped car, which never reaches the total laps, stays in play: a failure or accident after passing the line left it stopped and retired (state `+0x12C` = 3), and the classification and points counted it as "Out of race".
- **Now:** `BANDERA_CRUCE` (`0x00449D0E`) marks in an own 22-element table every car that crosses the line with the leader already in the list, or with the total laps done, or at 2 hours; on the first crossing of the race it clears the table. `BANDERA_FIN` (`0x0044A637`, the race closing) sets state 0 and reason 0 for the marked cars that are retired, as the game does for a car that finishes the distance, and clears the table. The car stays stopped on the track but counts as classified with the laps it did. Option `--sin-bandera-cuadros`. On by default in the generator.
- **Tests:** `probar_bandera_cuadros.py` (emulator, 427 tests: marks in each case and only in them, clearing on the first crossing, states and reasons at the closing, original prologue, registers and table).
- **Limits [I]:** until the race ends the panel still shows it retired; the retirement news and the season marks of the failure (`FUN_0045FB9D`, `0x00710FF8`) are not undone.
- **Status:** *Test*. Not yet seen in the game.

*Note (04/11/2026, afternoon):* the candidate `699267b2…` and the SC100 `0c84f047…` are installed with entries 24 to 44 (the candidate once the game was closed).

### 57. The AI order ladder in a single cave: one drop per order and lap (Test)

- **Ferrim's observation (08/11/2026, Great Britain):** the order descent felt faster than entry 39 said. Checked in the running game: Nakano and Tuero (Minardi) had almost every order at 1 and their brakes were wearing about 3.5 per lap against about 16 at the start.
- **Cause [L]:** the six caves of entries 39 and 40 were independent and each dropped 1 per lap, so a shared order dropped several times per lap: Acceleration hangs from clutch, gearbox and throttle (up to 3 points per lap); Braking, from brakes and clutch (up to 2); KerbUse, from suspension and gearbox (up to 2).
- **Now:** `ORDENES_IA_ESCALERA` (`0x0045BE77`, the common tail of `FUN_0045B21E`, the only path to its `RET`, after all counters are updated): for each order it takes the lowest target of the rules that touch it (the same 800, 700, 600, 500 and 400 to 5, 4, 3, 2 and 1 ladder) and drops it 1 at most per lap if it is above. Defl is not touched and neither are humans. `ORDENES_IA_FRENOS`, `ORDENES_IA_SUSPENSION` and `ORDENES_IA_EMBRAGUE` no longer contain the ladder: they only skip the original below-400 block. The options `--sin-ordenes-ia-adaptativas` and `--sin-ordenes-ia-cambio-hidraulica-acelerador` each remove their three rules from the single cave.
- **Tests:** `probar_ordenes_ia.py` (emulator, 1,211 tests: 600 random scenarios against the model with the six rules and seven orders, registers and stack, humans unchanged, Acceleration with three rules dropping 1 and not 3, the 12-lap sequence and the three skipped blocks).
- **Expected effect [I]:** shared orders drop more slowly than with entries 39 and 40; cars with several low parts take more laps to reach their target, so they wear a bit more part and perform a bit better. Not measured.
- **Not covered:** recovering the orders if the counter goes up after a pit-lane service (not done).
- **Status:** *Test*. Built on 08/11/2026; not installed.

### 58. Pit lane: Austria lane factor 0.58 (Test)

- **Ferrim's observation (09/11/2026):** in Austria Rosset lost 9 s on the in-lap and 16 s on the out-lap (25 s in total with the general factor of 0.70), and Ferrim believes real data exceeds half a minute.
- **Now:** `FACTORES_CARRIL_CIRCUITO[9]` goes from the general factor (0.70) to 0.58 (the ratio inside the lane drops, the pass is slower). With the model loss = c + natural / factor, a standing time of about 6.2 s and a natural transit of about 13 s, the loss goes from about 25 s to about 29 s [I]; 31 s would need 0.53.
- **Status:** *Test*. Built on 09/11/2026; not installed. To be checked in the next Austria race with the loss measured by laps; no real Austria data of our own.
