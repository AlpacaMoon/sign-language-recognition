# Sign Language to Text Translator
This is a local executable app written in Python and KivyMD that allows you to perform American Sign Languages (ASL) in front of your webcam and translates them into text or audio outputs.

This application makes no outbound calls for any record keeping or tracking.

## Features
- Translate static signs (26 alphabets & the numbers 1-10)
- Translate dynamic signs ([121 words](#Dynamic Sign Vocabulary))
- Convert raw output to fluent human-readable sentences
- Concatenate single characters from static signs into words
- Language translation
- Text-to-Speech


## Installation
This application was developed and tested on Python 3.9. We do not guarantee its compatibility in the future.

To run the source code, you need to download the dependencies listed in `requirements.txt`.
```
py -3.9 -m pip install -r "../requirements.txt"
```
Then simply run the `kivy_main.py` file.


## Dynamic Sign Vocabulary
The application is capable of recognising 121 words for now, and the model is trained using our own data created according to [HandSpeak](https://www.handspeak.com/ "HandSpeak"). 

| No | Word | Definition Reference | Video Reference |
| ------------ | ------------ | ------------ | ------------ |
| 1 | hello | https://www.handspeak.com/word/1015/ | https://www.handspeak.com/word/h/hel/hello.mp4 |
| 2 | good / thank | https://www.handspeak.com/word/2186/ | https://www.handspeak.com/word/t/tha/thank.mp4 |
| 3 | help | https://www.handspeak.com/word/1017/ | https://www.handspeak.com/word/h/hel/help.mp4 |
| 4 | I/me | https://www.handspeak.com/word/1086/ | https://www.handspeak.com/word/i/i-me.mp4 |
| 5 | please | https://www.handspeak.com/word/1658/ | https://www.handspeak.com/word/p/ple/please.mp4 |
| 6 | sorry | https://www.handspeak.com/word/2027/ | https://www.handspeak.com/word/s/sor/sorry.mp4 |
| 7 | welcome | https://www.handspeak.com/word/2380/ | https://www.handspeak.com/word/w/wel/welcome.mp4 |
| 8 | welcome | https://www.handspeak.com/word/2380/ | https://www.handspeak.com/word/w/wel/welcome2.mp4 |
| 9 | ok | https://www.handspeak.com/word/1545/ | https://www.handspeak.com/word/o/ok.mp4 |
| 10 | what | https://www.handspeak.com/word/2383/ | https://www.handspeak.com/word/w/wha/what.mp4 |
| 11 | what | https://www.handspeak.com/word/2383/ | https://www.handspeak.com/word/w/wha/what2.mp4 |
| 12 | can | https://www.handspeak.com/word/307/ | https://wwwhandspeak.com/word/c/can/can.mp4 |
| 13 | thank you very much | https://www.handspeak.com/word/2186/ | https://www.handspeak.com/word/t/tha/thank.mp4 |
| 14 | deaf | https://www.handspeak.com/word/539/ | https://www.handspeak.com/word/d/dea/deaf.mp4 |
| 15 | do not | https://www.handspeak.com/word/600/ | https://www.handspeak.com/word/d/do/do-not.mp4 |
| 16 | feel | https://www.handspeak.com/word/768/ | https://www.handspeak.com/word/f/fee/feel.mp4 |
| 17 | eat/food | https://www.handspeak.com/word/645/ | https://www.handspeak.com/word/e/eat/eat.mp4 |
| 18 | eat a lot | https://www.handspeak.com/word/645/ | https://www.handspeak.com/word/e/eat/eat-alot.mp4 |
| 19 | tired | https://www.handspeak.com/word/2225/ | https://www.handspeak.com/word/t/tir/tired.mp4 |
| 20 | because | https://www.handspeak.com/word/172/ | https://www.handspeak.com/word/b/bec/because.mp4 |
| 21 | sick | https://www.handspeak.com/word/1959/ | https://www.handspeak.com/word/s/sic/sick.mp4 |
| 22 | drink | https://www.handspeak.com/word/627/ | https://www.handspeak.com/word/d/dri/drink.mp4 |
| 23 | drink | https://www.handspeak.com/word/627/ | https://www.handspeak.com/word/d/dri/drink-plu.mp4 |
| 24 | apple | https://www.handspeak.com/word/97/ | https://www.handspeak.com/word/a/app/apple.mp4 |
| 25 | banana | https://www.handspeak.com/word/156/ | https://www.handspeak.com/word/b/ban/banana.mp4 |
| 26 | drive | https://www.handspeak.com/word/630/ | https://www.handspeak.com/word/d/dri/drive.mp4 |
| 27 | again | https://www.handspeak.com/word/51/ | https://www.handspeak.com/word/a/aga/again.mp4 |
| 28 | also | https://www.handspeak.com/word/69/ | https://www.handspeak.com/word/a/also.mp4 |
| 29 | ask | https://www.handspeak.com/word/117/ | https://www.handspeak.com/word/a/ask/ask.mp4 |
| 30 | yes | https://www.handspeak.com/word/2443/ | https://www.handspeak.com/word/y/yes/yes.mp4 |
| 31 | no | https://www.handspeak.com/word/1496/ | https://www.handspeak.com/word/n/no/no.mp4 |
| 32 | man | https://www.handspeak.com/word/1339/ | https://www.handspeak.com/word/m/man/man.mp4 |
| 33 | man | https://www.handspeak.com/word/1339/ | https://www.handspeak.com/word/m/man/man2.mp4 |
| 34 | woman | https://www.handspeak.com/word/2415/ | https://www.handspeak.com/word/w/wom/woman.mp4 |
| 35 | woman | https://www.handspeak.com/word/2415/ | https://www.handspeak.com/word/w/wom/woman2.mp4 |
| 36 | he/she | https://www.handspeak.com/word/1671/ | https://www.handspeak.com/word/h/he.mp4 |
| 37 | bad | https://www.handspeak.com/word/150/ | https://www.handspeak.com/word/b/bad/bad.mp4 |
| 38 | have/has/had | https://www.handspeak.com/word/989/ | https://www.handspeak.com/word/h/hav/have2.mp4 |
| 39 | have/has/had | https://www.handspeak.com/word/989/ | https://www.handspeak.com/word/h/hav/have.mp4 |
| 40 | when | https://www.handspeak.com/word/2390/ | https://www.handspeak.com/word/w/whe/when.mp4 |
| 41 | where | https://www.handspeak.com/word/2391/ | https://www.handspeak.com/word/w/whe/where2.mp4 |
| 42 | which | https://www.handspeak.com/word/2393/ | https://www.handspeak.com/word/w/whi/which.mp4 |
| 43 | who | https://www.handspeak.com/word/2398/ | https://www.handspeak.com/word/w/who/who.mp4 |
| 44 | why | https://www.handspeak.com/word/2399/ | https://www.handspeak.com/word/w/why/why.mp4 |
| 45 | how | https://www.handspeak.com/word/1067/ | https://www.handspeak.com/word/h/how/how.mp4 |
| 46 | you | https://www.handspeak.com/word/2448/ | https://www.handspeak.com/word/y/you/you.mp4 |
| 47 | boy | https://www.handspeak.com/word/223/ | https://www.handspeak.com/word/b/boy/boy.mp4 |
| 48 | girl | https://www.handspeak.com/word/908/ | https://www.handspeak.com/word/g/gir/girl.mp4 |
| 49 | friend | https://www.handspeak.com/word/865/ | https://www.handspeak.com/word/f/fri/friend.mp4 |
| 50 | finish/complete | https://www.handspeak.com/word/4917/ | https://www.handspeak.com/word/f/fin/finish2.mp4 |
| 51 | find | https://www.handspeak.com/word/2746/ | https://www.handspeak.com/word/f/fin/find.mp4 |
| 52 | other | https://www.handspeak.com/word/1582/ | https://www.handspeak.com/word/o/oth/other.mp4 |
| 53 | forget | https://www.handspeak.com/word/4917/ | https://www.handspeak.com/word/f/for/forget-disappear.mp4 |
| 54 | give | https://www.handspeak.com/word/910/ | https://www.handspeak.com/word/g/giv/give2.mp4 |
| 55 | give you | https://www.handspeak.com/word/910/ | https://www.handspeak.com/word/g/giv/give-you.mp4 |
| 56 | give me | https://www.handspeak.com/word/910/ | https://www.handspeak.com/word/g/giv/give-me.mp4 |
| 57 | go | https://www.handspeak.com/word/918/ | https://www.handspeak.com/word/g/go/go-to.mp4 |
| 58 | get | https://www.handspeak.com/word/901/ | https://www.handspeak.com/word/g/get/get.mp4 |
| 59 | understand/comprehend | https://www.handspeak.com/word/2292/ | https://www.handspeak.com/word/u/und/understand.mp4 |
| 60 | use | https://www.handspeak.com/word/2307/ | https://www.handspeak.com/word/u/use/use.mp4 |
| 61 | will | https://www.handspeak.com/word/2401/ | https://www.handspeak.com/word/w/wil/will.mp4 |
| 62 | with | https://www.handspeak.com/word/2412/ | https://www.handspeak.com/word/w/wit/with.mp4 |
| 63 | wait | https://www.handspeak.com/word/2341/ | https://www.handspeak.com/word/w/wai/wait.mp4 |
| 64 | work | https://www.handspeak.com/word/2423/ | https://www.handspeak.com/word/w/wor/work.mp4 |
| 65 | they | https://www.handspeak.com/word/2195/ | https://www.handspeak.com/word/t/the/they.mp4 |
| 66 | their | https://www.handspeak.com/word/2715/ | https://www.handspeak.com/word/t/the/their.mp4 |
| 67 | school | https://www.handspeak.com/word/1889/ | https://www.handspeak.com/word/s/sch/school.mp4 |
| 68 | write | https://www.handspeak.com/word/2436/ | https://www.handspeak.com/word/w/wri/write.mp4 |
| 69 | send text/message | https://www.handspeak.com/word/2114/ | https://www.handspeak.com/word/t/tex/text-send.mp4 |
| 70 | email | https://www.handspeak.com/word/659/ | https://www.handspeak.com/word/e/ema/email-verb.mp4 |
| 71 | email | https://www.handspeak.com/word/659/ | https://www.handspeak.com/word/e/ema/email.mp4 |
| 72 | home | https://www.handspeak.com/word/1046/ | https://www.handspeak.com/word/h/hom/home.mp4 |
| 73 | but | https://www.handspeak.com/word/290/ | https://www.handspeak.com/word/b/but/but.mp4 |
| 74 | should | https://www.handspeak.com/word/1952/ | https://www.handspeak.com/word/s/sho/should.mp4 |
| 75 | not | https://www.handspeak.com/word/1515/ | https://www.handspeak.com/word/n/not/not.mp4 |
| 76 | my | https://www.handspeak.com/word/1448/ | https://www.handspeak.com/word/m/my.mp4 |
| 77 | name | https://www.handspeak.com/word/1464/ | https://www.handspeak.com/word/n/nam/name.mp4 |
| 78 | like | https://www.handspeak.com/word/1276/ | https://www.handspeak.com/word/l/lik/like.mp4 |
| 79 | say | https://www.handspeak.com/word/1881/ | https://www.handspeak.com/word/s/say/say.mp4 |
| 80 | cold | https://www.handspeak.com/word/416/ | https://www.handspeak.com/word/c/col/cold-brr.mp4 |
| 81 | hot | https://www.handspeak.com/word/1060/ | https://www.handspeak.com/word/h/hot/hot2.mp4 |
| 82 | family | https://www.handspeak.com/word/740/ | https://www.handspeak.com/word/f/fam/family.mp4 |
| 83 | mother | https://www.handspeak.com/word/1439/ | https://www.handspeak.com/word/m/mot/mother.mp4 |
| 84 | father | https://www.handspeak.com/word/758/ | https://www.handspeak.com/word/f/fat/father.mp4 |
| 85 | many | https://www.handspeak.com/word/1347/ | https://www.handspeak.com/word/m/man/many.mp4 |
| 86 | few | https://www.handspeak.com/word/780/ | https://www.handspeak.com/word/f/few/few.mp4 |
| 87 | now | https://www.handspeak.com/word/1521/ | https://www.handspeak.com/word/n/now/now.mp4 |
| 88 | later | https://www.handspeak.com/word/5683/ | https://www.handspeak.com/word/l/lat/later.mp4 |
| 89 | time | https://www.handspeak.com/word/2223/ | https://www.handspeak.com/word/t/tim/time2.mp4 |
| 90 | tomorrow | https://www.handspeak.com/word/2233/ | https://www.handspeak.com/word/t/tom/tomorrow.mp4 |
| 91 | yesterday | https://www.handspeak.com/word/2444/ | https://www.handspeak.com/word/y/yes/yesterday.mp4 |
| 92 | same/also | https://www.handspeak.com/word/2628/ | https://www.handspeak.com/word/s/sam/same-also.mp4 |
| 93 | remember | https://www.handspeak.com/word/1797/ | https://www.handspeak.com/word/r/rem/remember.mp4 |
| 94 | your | https://www.handspeak.com/word/2453/ | https://www.handspeak.com/word/y/you/your.mp4 |
| 95 | more | https://www.handspeak.com/word/1433/ | https://www.handspeak.com/word/m/mor/more.mp4 |
| 96 | meet | https://www.handspeak.com/word/1371/ | https://www.handspeak.com/word/m/mee/meet.mp4 |
| 97 | see | https://www.handspeak.com/word/1911/ | https://www.handspeak.com/word/s/see/see.mp4 |
| 98 | slow | https://www.handspeak.com/word/1992/ | https://www.handspeak.com/word/s/slo/slow.mp4 |
| 99 | fast/quick | https://www.handspeak.com/word/754/ | https://www.handspeak.com/word/f/fas/fast-quick.mp4 |
| 100 | some | https://www.handspeak.com/word/2019/ | https://www.handspeak.com/word/s/som/some.mp4 |
| 101 | store/shop | https://www.handspeak.com/word/2080/ | https://www.handspeak.com/word/s/sto/store.mp4 |
| 102 | take | https://www.handspeak.com/word/2144/ | https://www.handspeak.com/word/t/tak/take.mp4 |
| 103 | take/bring me | https://www.handspeak.com/word/2144/ | https://www.handspeak.com/word/t/tak/take-me.mp4 |
| 104 | tell | https://www.handspeak.com/word/2169/ | https://www.handspeak.com/word/t/tel/tell.mp4 |
| 105 | think | https://www.handspeak.com/word/2201/ | https://www.handspeak.com/word/t/thi/think.mp4 |
| 106 | want | https://www.handspeak.com/word/2347/ | https://www.handspeak.com/word/w/wan/want.mp4 |
| 107 | inexpensive | https://www.handspeak.com/word/366/ | https://www.handspeak.com/word/c/che/cheap.mp4 |
| 108 | expensive | https://www.handspeak.com/word/713/ | https://www.handspeak.com/word/e/exp/expensive.mp4 |
| 109 | that | https://www.handspeak.com/word/2782/ | https://www.handspeak.com/word/t/tha/that-inf.mp4 |
| 110 | this | https://www.handspeak.com/word/2786/ | https://www.handspeak.com/word/t/thi/this.mp4 |
| 111 | here | https://www.handspeak.com/word/1023/ | https://www.handspeak.com/word/h/her/here.mp4 |
| 112 | near | https://www.handspeak.com/word/2620/ | https://www.handspeak.com/word/n/nea/near.mp4 |
| 113 | far | https://www.handspeak.com/word/743/ | https://www.handspeak.com/word/f/far/far.mp4 |
| 114 | cat | https://www.handspeak.com/word/334/ | https://www.handspeak.com/word/c/cat/cat.mp4 |
| 115 | dog | https://www.handspeak.com/word/602/ | https://www.handspeak.com/word/d/dog/dog-fs.mp4 |
| 116 | morning | https://www.handspeak.com/word/1436/ | https://www.handspeak.com/word/m/mor/morning.mp4 |
| 117 | night | https://www.handspeak.com/word/1492/ | https://www.handspeak.com/word/n/nig/night.mp4 |
| 118 | beautiful | https://www.handspeak.com/word/171/ | https://www.handspeak.com/word/b/bea/beautiful.mp4 |
| 119 | open | https://www.handspeak.com/word/1561/ | https://www.handspeak.com/word/o/ope/open-frank.mp4 |
| 120 | close/shut | https://www.handspeak.com/word/407/ | https://www.handspeak.com/word/c/clo/close-hour.mp4 |
| 121 | close/shut | https://www.handspeak.com/word/407/ | https://www.handspeak.com/word/c/clo/close-hour2.mp4 |

## Static Sign Vocabulary
The application is capable of recognising 26 alphabets and 10 numbers from 1-10 for now, and the model is trained using our own data created according to [HandSpeak](https://www.handspeak.com/ "HandSpeak") for alphabets and [American Society for Deaf Children](https://deafchildren.org/ "American Society for Deaf Children") for numbers.

| No | Word  | Definition Reference                          |
|-------|-------|----------------------------------------------|
| 1     | A     | https://www.handspeak.com/word/2460/          |
| 2     | B     | https://www.handspeak.com/word/2461/          |
| 3     | C     | https://www.handspeak.com/word/2462/          |
| 4     | D     | https://www.handspeak.com/word/2463/          |
| 5     | E     | https://www.handspeak.com/word/2464/          |
| 6     | F     | https://www.handspeak.com/word/2465/          |
| 7     | G     | https://www.handspeak.com/word/2466/          |
| 8     | H     | https://www.handspeak.com/word/2467/          |
| 9     | I     | https://www.handspeak.com/word/2468/          |
| 10    | J     | https://www.handspeak.com/word/2469/          |
| 11    | K     | https://www.handspeak.com/word/2470/          |
| 12    | L     | https://www.handspeak.com/word/2471/          |
| 13    | M     | https://www.handspeak.com/word/2472/          |
| 14    | N     | https://www.handspeak.com/word/2473/          |
| 15    | O     | https://www.handspeak.com/word/2474/          |
| 16    | P     | https://www.handspeak.com/word/2475/          |
| 17    | Q     | https://www.handspeak.com/word/2476/          |
| 18    | R     | https://www.handspeak.com/word/2477/          |
| 19    | S     | https://www.handspeak.com/word/2478/          |
| 20    | T     | https://www.handspeak.com/word/2479/          |
| 21    | U     | https://www.handspeak.com/word/2480/          |
| 22    | V     | https://www.handspeak.com/word/2481/          |
| 23    | W     | https://www.handspeak.com/word/2482/          |
| 24    | X     | https://www.handspeak.com/word/2483/          |
| 25    | Y     | https://www.handspeak.com/word/2484/          |
| 26    | Z     | https://www.handspeak.com/word/2485/          |
| 27    | one   | https://deafchildren.org/2019/07/free-asl-numbers-chart/ |
| 28    | two   | https://deafchildren.org/2019/07/free-asl-numbers-chart/ |
| 29    | three | https://deafchildren.org/2019/07/free-asl-numbers-chart/ |
| 30    | four  | https://deafchildren.org/2019/07/free-asl-numbers-chart/ |
| 31    | five  | https://deafchildren.org/2019/07/free-asl-numbers-chart/ |
| 32    | six   | https://deafchildren.org/2019/07/free-asl-numbers-chart/ |
| 33    | seven | https://deafchildren.org/2019/07/free-asl-numbers-chart/ |
| 34    | eight | https://deafchildren.org/2019/07/free-asl-numbers-chart/ |
| 35    | nine  | https://deafchildren.org/2019/07/free-asl-numbers-chart/ |
| 36    | ten   | https://deafchildren.org/2019/07/free-asl-numbers-chart/ |
