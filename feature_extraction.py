import re
import pandas as pd
import csv

words = [
    "mischievous",
    "mischievious",
    "realtor(s)?",
    "estate agent(s)?",
    "spigot(s)?",
    "spicket(s)?",
    "dragged",
    "drug",
    "you all",
    "(yous)|(youse)",
    "yins",
    "you lot",
    "you guys",
    "you uns",
    "y all",
    "tag sale(s)?",
    "yard sale(s)?",
    "garage sale(s)?",
    "rummage sale(s)?",
    "thrift sale(s)?",
    "stoop sale(s)?",
    "car port sale(s)?",
    "side walk sale(s)?",
    "jumble sale(s)?",
    "car boot sale(s)?",
    "patio sale(s)?",
    "mumblety peg(s)?",
    "mumbledy peg(s)?",
    "mumbly peg(s)?",
    "mumblely peg(s)?",
    "mumble peg(s)?",
    "mummety peg(s)?",
    "numblety peg(s)?",
    "base ball jack knife",
    "stick knife",
    "stick frog(s)?",
    "stretch",
    "knifey",
    "splits",
    "sub(s)?",
    "grinder(s)?",
    "hoagie(s)?",
    "po[or]? boy(s)?",
    "Italian sandwich(es)?",
    "sarney(s)?",
    "fire fl(y|ies)",
    "lightning bug(s)?",
    "craw fish(es)?",
    "cray fish(es)?",
    "craw dad(s)?",
    "daddy long leg(s)?",
    "daddy big leg(s)?",
    "daddy bug(s)?",
    "father long leg(s)?",
    "daddy gray beard(s)?",
    "harvest man",
    "moskeet spider(s)?",
    "grand mother(s)?",
    "granny(s)?",
    "grandma(s)?",
    "nana(s)?",
    "gramm[y|i](s)?",
    "gramma(s)?",
    "gramps",
    "grandpa(s)?",
    "grampa(s)?",
    "grand[d]?ad(s)?",
    "pap(s)?",
    "dust bunnies",
    "dust kittens",
    "dust mice",
    "dust balls",
    "sneaker(s)?",
    "gym shoe(s)?",
    "sand shoe(s)?",
    "jumper(s)?",
    "tennis shoe(s)?",
    "running shoe(s)?",
    "pill bug(s)?",
    "doodle bug(s)?",
    "potato bug(s)?",
    "roly pol[y|ies]",
    "sow bug(s)?",
    "basket ball bug(s)?",
    "twiddle bug(s)?",
    "roll up bug(s)?",
    "wood louse(s)?",
    "shopping cart(s)?",
    "shopping wagon(s)?",
    "grocery cart(s)?",
    "shopping carriage(s)?",
    "super market trolley(s)?",
    "kitty corner(s)?",
    "kita corner(s)?",
    "cater corner(s)?",
    "catty corner(s)?",
    "kitty cross",
    "kitty wampus",
    "[(do)|(did)|(done)|(doing)|(does)] donuts",
    "[(do)|(did)|(done)|(doing)|(does)] cookies",
    "[(whip)|(whipped)|(whips)|(whipping)] shitties",
    "sun shower(s)?",
    "wolf is giving birth",
    "devil is beating his wife",
    "monkey s wedding(s)?",
    "fox s wedding(s)?",
    "pine apple rain",
    "liquid sun",
    "goose bump(s)?",
    "goose flesh",
    "goose pimple(s)?",
    "chill bump(s)?",
    "chill bug(s)?",
    "chilly bump(s)?",
    "cold chill bump(s)?",
    "rotary",
    "round about(s)?",
    "traffic circle(s)?",
    "traffic circus(es)?",
    "hair elastic(s)?",
    "hair tie(s)?",
    "cruller(s)?",
    "bear claw(s)?",
    "cole slaw",
    "^(?!cole slaw).*\\bslaw\\b",
    "vinegar and oil",
    "oil and vinegar",
    "by accident",
    "on accident",
    "cut[ting]? the grass",
    "cut[ting]? the lawn",
    "mow[(ed)|(ing)] the grass",
    "mow[(ed)|(ing)] the lawn",
    "water bug(s)?",
    "jesus bug(s)?",
    "water strider(s)?",
    "back strider(s)?",
    "^(?!water strider)(?!back strider).*\\bstrider(s)?\\b",
    "water spider(s)?",
    "water crawler(s)?",
    "water beetle(s)?",
    "skimmer(s)?",
    "^(?!water bubbler).*\\bbubbler(s)?\\b",
    "water bubbler(s)?",
    "drinking fountain(s)?",
    "water fountain(s)?",
    "the subway",
    "(the l)|(the el)",
    "the t",
    "the metro",
    "the bart",
    "soda(s)?",
    "pop",
    "coke(s)?",
    "tonic(s)?",
    "soft drink(s)?",
    "cocola(s)?",
    "fizzy drink(s)?",
    "gate night(s)?",
    "trick night(s)?",
    "mischief night(s)?",
    "cabbage night(s)?",
    "goosey night(s)?",
    "devil s night(s)?",
    "devil s eve(s)?",
    "moot point(s)?",
    "mute point(s)?",
    "brew thru(s)?",
    "party barn(s)?",
    "boot legger(s)?",
    "beer barn(s)?",
    "beverage barn(s)?",
    "carry out",
    "take out",
    "ogl[e|es|ed|ing]",
    "oogl[e|es|ed|ing]",
    "oggl[e|es|ed|ing]",
]

multiple_modals = [
    "better can",
    "can might",
    "can( )?t never would",
    "could might",
    "may can",
    "may can( )?t",
    "may not can",
    "may could",
    "may couldn( )?t",
    "may did",
    "may didn( )?t",
    "may might",
    "may might can",
    "may need to",
    "may not can",
    "may not could",
    "may shall",
    "may should",
    "may shouldn( )?t",
    "may supposed to",
    "may use(ta|d to)",
    "may will",
    "may will can()?t",
    "may won( )?t",
    "may would",
    "might better",
    "might can",
    "might could",
    "might couldn( )?t",
    "might did",
    "might had better",
    "might (have|ve) use(ta|d to)",
    "might not can",
    "might not could",
    "might not should",
    "might not shouldn( )?t",
    "might not would",
    "might should",
    "might should better",
    "might shouldn( )?t",
    "might should ought(a| to)",
    "might supposed to",
    "might will",
    "might will can( )?t",
    "might would",
    "might wouldn( )?t",
    "might would(a| have|( )?ve) had ought(a| to)",
    "might ought((a)| to)",
    "must(a| have) could(a| have|( )?ve)",
    "must didn( )?t",
    "ought(a| to) could",
    "should might better",
    "should ought((a)| to)",
    "shouldn( )?t ought((a)| to)",
    "use(ta|d to) could",
    "use(ta|d to) did",
    "use(ta|d to) didn( )?t",
    "use(ta|d to) (gon(na)?|going to)",
    "use(ta|d to) wasn( )?t",
    "use(ta|d to) wouldn( )?t",
    "would might",
    "would better",
]

drug_exceptions = [53961, 73120, 75110, 101868]

def build_regex():
    regex = {}  # key = string, value = regex
    for w in words:
        # replacing spaces with optional whitespace 
        reformatted_w = "\\s*".join(w.split())

        # requiring that matched patterns be separate from other words
        if w[0] != "^":
            reformatted_w = "\\b" + reformatted_w + "\\b"
        
        regex[w] = re.compile(reformatted_w)

    giant_modal_regex = ""
    for m in multiple_modals:
        # requiring that matched patterns be separate from other words
        giant_modal_regex += "(\\b" + m + "\\b)|"
    giant_modal_regex = giant_modal_regex[:-1]
    
    regex["modals"] = re.compile(giant_modal_regex)
    return regex


def extract_features(feat_names, regex, text, i):
    feats = []
    for f in feat_names:
        if re.search(regex[f], text):

            # kludge to avoid having to do POS tagging on drug
            if f == "drug": 
                if i in drug_exceptions:
                    feats.append(1)
                    print(text)
                else:
                    feats.append(0)
            
            else: 
                feats.append(1)

        else:
            feats.append(0)
    return feats



if __name__ == '__main__':
    regex = build_regex()
    cols = ["state"] + list(regex.keys())

    ensemble_data_path = 'ensemble2.csv'
    ensemble = pd.read_csv(ensemble_data_path)

    with open('features.csv', 'w') as csv_file:
        csv_file = csv.writer(csv_file)
        csv_file.writerow(cols)
        for i in range(ensemble.shape[0]):
            text = ensemble["text"][i]
            features = extract_features(cols[1:], regex, text, i)
            csv_file.writerow([ensemble["state"][i]] + features)
            # if i % 1000 == 0: print(i)
