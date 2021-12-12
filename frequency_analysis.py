from collections import defaultdict, Counter
import pandas as pd
import json
from matplotlib import pyplot as plt
import re
import random

word_clusters = [
    ["mischievous", "mischievious"],
    ["realtor(s)?", "estate agent(s)?"],
    ["spigot(s)?", "spicket(s)?"],
    ["dragged", "drug"],
    ["you all", "(yous)|(youse)", "yins", "you lot", "you guys", "you uns", "y all"],
    ["tag sale(s)?", "yard sale(s)?", "garage sale(s)?", "rummage sale(s)?", "thrift sale(s)?", "stoop sale(s)?", "car port sale(s)?", "side walk sale(s)?", "jumble sale(s)?", "car boot sale(s)?", "patio sale(s)?"],
    ["mumblety peg(s)?", "mumbledy peg(s)?", "mumbly peg(s)?", "mumblely peg(s)?", "mumble peg(s)?", "mummety peg(s)?", "numblety peg(s)?", "base ball jack knife", "stick knife", "stick frog(s)?", "knifey"],
    ["sub(s)?", "hoagie(s)?", "po[or]? boy(s)?", "Italian sandwich(es)?", "sarney(s)?"],
    ["fire fl(y|ies)", "lightning bug(s)?"],
    ["craw fish(es)?", "cray fish(es)?", "craw dad(s)?"],
    ["daddy long leg(s)?", "daddy big leg(s)?", "daddy bug(s)?", "father long leg(s)?", "daddy gray beard(s)?", "harvest man", "moskeet spider(s)?"],
    ["grand mother(s)?", "grann[y|ie](s)?", "grandma(s)?", "nana(s)?", "gramm[y|i|ies](s)?", "gramma(s)?"],
    ["gramps", "grandpa(s)?", "grampa(s)?", "grand[d]?ad(s)?", "pap(s)?"],
    ["dust bunnies", "dust kittens", "dust mice", "dust balls"],
    ["sneaker(s)?", "gym shoe(s)?", "sand shoe(s)?", "jumper(s)?", "tennis shoe(s)?", "running shoe(s)?"],
    ["pill bug(s)?", "doodle bug(s)?", "potato bug(s)?", "roly pol[y|ies]", "sow bug(s)?", "basket ball bug(s)?", "twiddle bug(s)?", "roll up bug(s)?", "wood louse(s)?"],
    ["shopping cart(s)?", "shopping wagon(s)?", "grocery cart(s)?", "shopping carriage(s)?", "super market trolley(s)?"],
    ["kitty corner(s)?", "kita corner(s)?", "cater corner(s)?", "catty corner(s)?", "kitty cross", "kitty wampus"],
    ["[(do)|(did)|(done)|(doing)|(does)] donuts", "[(do)|(did)|(done)|(doing)|(does)] cookies", "[(whip)|(whipped)|(whips)|(whipping)] shitties"],
    ["sun shower(s)?", "wolf is giving birth", "devil is beating his wife", "monkey s wedding(s)?", "fox s wedding(s)?", "pine apple rain", "liquid sun"],
    ["goose bump(s)?", "goose flesh", "goose pimple(s)?", "chill bump(s)?", "chill bug(s)?", "chilly bump(s)?", "cold chill bump(s)?"],
    ["rotary", "round about(s)?", "traffic circle(s)?", "traffic circus(es)?"],
    ["hair elastic(s)?", "hair tie(s)?"],
    ["cruller(s)?"],
    ["bear claw(s)?"],
    ["cole slaw", "^(?!cole slaw).*\\bslaw\\b"],
    ["vinegar and oil", "oil and vinegar"],
    ["by accident", "on accident"],
    ["cut[ting]? the grass", "cut[ting]? the lawn", "mow[(ed)|(ing)] the grass", "mow[(ed)|(ing)] the lawn"],
    ["water bug(s)?", "jesus bug(s)?", "water strider(s)?", "back strider(s)?", "^(?!water strider)(?!back strider).*\\bstrider(s)?\\b", "water spider(s)?", "water crawler(s)?", "water beetle(s)?", "skimmer(s)?"],
    ["^(?!water bubbler).*\\bbubbler(s)?\\b", "water bubbler(s)?", "drinking fountain(s)?", "water fountain(s)?"],
    ["the subway", "the t", "the metro", "the bart"],
    ["soda(s)?", "pop", "coke(s)?", "tonic(s)?", "soft drink(s)?", "cocola(s)?", "fizzy drink(s)?"],
    ["gate night(s)?", "trick night(s)?", "mischief night(s)?", "cabbage night(s)?", "goosey night(s)?", "devil s night(s)?", "devil s eve(s)?"],
    ["moot point(s)?", "mute point(s)?"],
    ["brew thru(s)?", "party barn(s)?", "boot legger(s)?", "beer barn(s)?", "beverage barn(s)?"],
    ["carry out", "take out"],
    ["ogl[e|es|ed|ing]", "oogl[e|es|ed|ing]", "oggl[e|es|ed|ing]"],
    ["modals"],
]

label_key = {
    "mischievous" : "mischievous",
    "mischievious" : "mischievious",
    "realtor(s)?" : "realtor",
    "estate agent(s)?" : "estate agent",
    "spigot(s)?" : "spigot",
    "spicket(s)?" : "spicket",
    "dragged" : "dragged",
    "drug" : "drug",
    "you all" : "you all",
    "(yous)|(youse)" : "yous",
    "yins" : "yins",
    "you lot" : "you lot",
    "you guys" : "you guys",
    "you uns" : "you uns",
    "y all" : "y'all",
    "tag sale(s)?" : "tag sale",
    "yard sale(s)?" : "yard sale",
    "garage sale(s)?" : "garage sale",
    "rummage sale(s)?" : "rummage sale",
    "thrift sale(s)?" : "thrift sale",
    "stoop sale(s)?" : "stoop sale",
    "car port sale(s)?" : "carport sale",
    "side walk sale(s)?" : "sidewalk sale",
    "jumble sale(s)?" : "jumble sale",
    "car boot sale(s)?" : "carboot sale",
    "patio sale(s)?" : "patio sale",
    "mumblety peg(s)?" : "mublety-peg",
    "mumbledy peg(s)?" : "mumbledy-peg",
    "mumbly peg(s)?" : "mumbly-peg",
    "mumblely peg(s)?" : "mumblely-peg",
    "mumble peg(s)?" : "muble-peg",
    "mummety peg(s)?" : "mummety-peg",
    "numblety peg(s)?" : "numblety-peg",
    "base ball jack knife" : "baseball jackknife",
    "stick knife" : "stickknife",
    "stick frog(s)?" : "stick frog",
    "knifey" : "knifey",
    "splits" : "splits",
    "sub(s)?" : "sub",
    "hoagie(s)?" : "hoagie",
    "po[or]? boy(s)?" : "poor boy",
    "Italian sandwich(es)?" : "Italian sandwich",
    "sarney(s)?" : "sarney",
    "fire fl(y|ies)" : "firefly",
    "lightning bug(s)?" : "lightning bug",
    "craw fish(es)?" : "crawfish",
    "cray fish(es)?" : "crayfish",
    "craw dad(s)?" : "crawdad",
    "daddy long leg(s)?" : "daddy long legs",
    "daddy big leg(s)?" : "daddy big legs",
    "daddy bug(s)?" : "daddy bug",
    "father long leg(s)?" : "father long legs",
    "daddy gray beard(s)?" : "daddy greybeards",
    "harvest man" : "harvestman",
    "moskeet spider(s)?" : "moskeet spider",
    "grand mother(s)?" : "grandmother",
    "grann[y|ie](s)?" : "granny",
    "grandma(s)?" : "grandma",
    "nana(s)?" : "nana",
    "gramm[y|i|ies](s)?" : "grammy",
    "gramma(s)?" : "gramma",
    "gramps" : "gramps",
    "grandpa(s)?" : "grandpa",
    "grampa(s)?" : "grampa",
    "grand[d]?ad(s)?" : "granddad",
    "pap(s)?" : "pap",
    "dust bunnies" : "dust bunnies",
    "dust kittens" : "dust kittens",
    "dust mice" : "dust mice",
    "dust balls" : "dustballs",
    "sneaker(s)?" : "sneakers",
    "gym shoe(s)?" : "gym shoes",
    "sand shoe(s)?" : "sand shoes",
    "jumper(s)?" : "jumpers",
    "tennis shoe(s)?" : "tennis shoes",
    "running shoe(s)?" : "running shoes",
    "pill bug(s)?" : "pill bug",
    "doodle bug(s)?" : "doodle bug",
    "potato bug(s)?" : "potato bug",
    "roly pol[y|ies]" : "roly poly",
    "sow bug(s)?" : "sow bug",
    "basket ball bug(s)?" : "basketball bug",
    "twiddle bug(s)?" : "twiddle bug",
    "roll up bug(s)?" : "roll-up bug",
    "wood louse(s)?" : "wood louse",
    "shopping cart(s)?" : "shopping cart",
    "shopping wagon(s)?" : "shopping wagon",
    "grocery cart(s)?" : "grocery cart",
    "shopping carriage(s)?" : "shopping carriage",
    "super market trolley(s)?" : "supermarket trolley",
    "kitty corner(s)?" : "kitty corner",
    "kita corner(s)?" : "kitacorner",
    "cater corner(s)?" : "catercorner",
    "catty corner(s)?" : "cattycorner",
    "kitty cross" : "kitty cross",
    "kitty wampus" : "kitty wampus",
    "[(do)|(did)|(done)|(doing)|(does)] donuts" : "doing donuts",
    "[(do)|(did)|(done)|(doing)|(does)] cookies" : "doing cookies",
    "[(whip)|(whipped)|(whips)|(whipping)] shitties" : "whipping shitties",
    "sun shower(s)?" : "sunshower",
    "wolf is giving birth" : "wolf is giving birth",
    "devil is beating his wife" : "devil is beating his wife",
    "monkey s wedding(s)?" : "monkey's wedding",
    "fox s wedding(s)?" : "fox's wedding",
    "pine apple rain" : "pineapple rain",
    "liquid sun" : "liquid sun",
    "goose bump(s)?" : "goosebumps",
    "goose flesh" : "gooseflesh",
    "goose pimple(s)?" : "goose pimples",
    "chill bump(s)?" : "chill bumps",
    "chill bug(s)?" : "chill bugs",
    "chilly bump(s)?" : "chilly bumps",
    "cold chill bump(s)?" : "cold-chill bumps",
    "rotary" : "rotary",
    "round about(s)?" : "roundabout",
    "traffic circle(s)?" : "traffic circle",
    "traffic circus(es)?" : "traffic circus",
    "hair elastic(s)?" : "hair elastic",
    "hair tie(s)?" : "hair tie",
    "cruller(s)?" : "cruller",
    "bear claw(s)?" : "bearclaw",
    "cole slaw" : "coleslaw",
    "^(?!cole slaw).*\\bslaw\\b" : "slaw",
    "vinegar and oil" : "vinegar and oil",
    "oil and vinegar" : "oil and vinegar",
    "by accident" : "by accident",
    "on accident" : "on accident",
    "cut[ting]? the grass" : "cut the grass",
    "cut[ting]? the lawn" : "cut the lawn",
    "mow[(ed)|(ing)] the grass" : "mow the grass",
    "mow[(ed)|(ing)] the lawn" : "mow the lawn",
    "water bug(s)?" : "water bug",
    "jesus bug(s)?" : "Jesus bug",
    "water strider(s)?" : "waterstrider",
    "back strider(s)?" : "backstrider",
    "^(?!water strider)(?!back strider).*\\bstrider(s)?\\b" : "strider",
    "water spider(s)?" : "water spider",
    "water crawler(s)?" : "water crawler",
    "water beetle(s)?" : "water beetle",
    "skimmer(s)?" : "skimmer",
    "^(?!water bubbler).*\\bbubbler(s)?\\b" : "bubbler",
    "water bubbler(s)?" : "water bubbler",
    "drinking fountain(s)?" : "drinking fountain",
    "water fountain(s)?" : "water fountain",
    "the subway" : "the subway",
    "the t" : "the T",
    "the metro" : "the Metro",
    "the bart" : "the BART",
    "soda(s)?" : "soda",
    "pop" : "pop",
    "coke(s)?" : "coke",
    "tonic(s)?" : "tonic",
    "soft drink(s)?" : "soft drink",
    "cocola(s)?" : "cocola",
    "fizzy drink(s)?" : "fizzy drink",
    "gate night(s)?" : "gate night",
    "trick night(s)?" : "trick night",
    "mischief night(s)?" : "mischief night",
    "cabbage night(s)?" : "cabbage night",
    "goosey night(s)?" : "goosey night",
    "devil s night(s)?" : "devil's night",
    "devil s eve(s)?" : "devil's eve",
    "moot point(s)?" : "moot point",
    "mute point(s)?" : "mute point",
    "brew thru(s)?" : "brew thru",
    "party barn(s)?" : "party barn",
    "boot legger(s)?" : "bootlegger",
    "beer barn(s)?" : "beer barn",
    "beverage barn(s)?" : "beverage barn",
    "carry out" : "carry-out",
    "take out" : "take-out",
    "ogl[e|es|ed|ing]" : "ogle",
    "oogl[e|es|ed|ing]" : "oogle",
    "oggl[e|es|ed|ing]" : "oggle",
    "modals" : "modals", 
}

state_list = ["MA", "OR", "TX", "FL", "GA", "OH", "CO", "WA"]

state_dict = {
    "MA" : "Massachusetts",
    "OR" : "Oregon",
    "TX" : "Texas",
    "FL" : "Florida",
    "GA" : "Georgia",
    "OH" : "Ohio",
    "CO" : "Colorado",
    "WA" : "Washington",
}

def count_regional_frequencies_clustered(features):

    regional_frequencies = defaultdict(lambda : defaultdict(lambda: defaultdict(lambda: 0)))
    
    for i in range(features.shape[0]):
    # for i in range(10):
        state = features["state"][i]
        for cluster_index, cluster in enumerate(word_clusters):
            for word in cluster:
                regional_frequencies[cluster_index][state][word] += int(features[word][i])
        if i % 1000 == 0: print(i)
    return regional_frequencies

def count_regional_frequencies_unclustered(features):
    regional_frequencies = defaultdict(lambda : defaultdict(lambda : 0))
    feat_list = list(features.columns)[1:]

    for i in range(features.shape[0]):
        state = features["state"][i]
        for f in feat_list:
            regional_frequencies[f][state] += int(features[f][i])
    return regional_frequencies

def csv_to_frequency_json(input_csv_name, output_name, clustering = True):
    features = pd.read_csv(input_csv_name)
    if clustering:
        regional_frequencies = count_regional_frequencies_clustered(features)
    else:
        regional_frequencies = count_regional_frequencies_unclustered(features)

    with open(output_name, "w") as outfile:
        json.dump(regional_frequencies, outfile, indent = 2)

def build_pie_charts(input_json_name):
    with open(input_json_name, 'r') as handle:
        regional_frequencies = json.load(handle)
    
    for cluster_num in regional_frequencies:
        for state in regional_frequencies[cluster_num]:
            if state in state_list:
                words = []
                counts = []
                for word in regional_frequencies[cluster_num][state]:
                    if regional_frequencies[cluster_num][state][word] > 0:
                        words.append(label_key[word])
                        counts.append(regional_frequencies[cluster_num][state][word])
                if len(words) > 0:
                    f = plt.pie(counts, labels = words, autopct='%1.0f%%')
                    plt.title("Yelp Data for " + state_dict[state] + ", n = " + str(sum(counts)))
                    plt.savefig("plots/plot_" + str(cluster_num) + "_" + state + ".png")
                    plt.clf()

def bootstrapping_trial(features, clusters):
    n = features.shape[0]
    
    regional_frequencies = defaultdict(lambda : defaultdict(lambda: defaultdict(lambda: 0)))    
    for iteration in range(n):
        i = random.randint(0,n-1)
        state = features["state"][i] 
        for cluster_i, cluster in enumerate(clusters):
            for w in cluster:
                regional_frequencies[cluster_i][state][w] += int(features[w][i])

    return regional_frequencies

def bootstrapping(features, clusters, output_name):
    totals = defaultdict(lambda : defaultdict(lambda: defaultdict(lambda: [])))

    for i in range(40):
        freqs = bootstrapping_trial(features, clusters)
        for c in freqs:
            for state in freqs[c]:
                total = sum(freqs[c][state].values())
                if total > 0:
                    for word in freqs[c][state]:
                        totals[c][state][word].append(freqs[c][state][word]/total)
    
    CI = defaultdict(lambda : defaultdict(lambda: defaultdict(lambda: [])))
    for c in totals:
        for state in totals[c]:
            for word in totals[c][state]:
                lst = totals[c][state][word]
                lst.sort()
                lower_bound = lst[2]
                upper_bound = lst[-3]
                CI[c][state][word] = [lower_bound, upper_bound]
    
    with open(output_name, "w") as outfile:
        json.dump(CI, outfile, indent = 2)

def frequencies_to_proportions(freqs):
    proportions = defaultdict(lambda : defaultdict(lambda: defaultdict(lambda: 0)))
    for c in freqs:
        for state in freqs[c]:
            total = sum(freqs[c][state].values())
            if total > 0:
                for word in freqs[c][state]:
                    proportions[c][state][word] = freqs[c][state][word]/total
    return proportions

def format_table(yelp_fn, yelp_ci_fn, harvard_fn, cluster_index, feature_names, output_name):
    with open(yelp_fn, 'r') as handle:
        yelp = json.load(handle)

    with open(yelp_ci_fn, 'r') as handle:
        yelp_ci = json.load(handle)
    
    with open(harvard_fn, 'r') as handle:
        harvard = json.load(handle)
    
    output = ""

    # build header
    output += "state\t"
    for feat in feature_names:
        output += feat + " Harvard\t" + "Yelp\t" + "Yelp CI\t"
    output += "\n"
    
    # data for each state
    for state in harvard[cluster_index]:
        output += state + "\t"
        
        for f in feature_names:
            harvard_proportion = harvard[cluster_index][state][f]
            harvard_proportion = str(round(harvard_proportion, 2))

            output += harvard_proportion + "\t"

            yelp_proportion = yelp[cluster_index][state][f]
            yelp_proportion = str(round(yelp_proportion, 2))

            output += yelp_proportion + "\t"

            yelp_ci_data = yelp_ci[cluster_index][state][f]
            yelp_lower_bound = str(round(yelp_ci_data[0], 2))
            yelp_upper_bound = str(round(yelp_ci_data[1], 2))

            output += "[" + yelp_lower_bound + ", " + yelp_upper_bound + "]\t"


        output += "\n"
    
    with open(output_name, "w") as handle:
        handle.write(output)
    


if __name__ == '__main__':
    # get training frequencies
    # csv_to_frequency_json("features.csv", "frequencies_clustered.json", clustering = True)
    # csv_to_frequency_json("features_train.csv", "frequencies_train_clustered.json", clustering = True)
    # csv_to_frequency_json("features_train.csv", "frequencies_train_unclustered.json", clustering = False)

    # clusters = [
    #     ["realtor(s)?", "estate agent(s)?"],
    #     ["you all", "(yous)|(youse)", "yins", "you lot", "you guys", "you uns", "y all"],
    #     ["sub(s)?", "hoagie(s)?", "po[or]? boy(s)?", "Italian sandwich(es)?", "sarney(s)?"],
    #     ["craw fish(es)?", "cray fish(es)?", "craw dad(s)?"],
    #     ["grand mother(s)?", "grann[y|ie](s)?", "grandma(s)?", "nana(s)?", "gramm[y|i|ies](s)?", "gramma(s)?"],
    #     ["sneaker(s)?", "gym shoe(s)?", "sand shoe(s)?", "jumper(s)?", "tennis shoe(s)?", "running shoe(s)?"],
    #     ["cole slaw", "^(?!cole slaw).*\\bslaw\\b"],
    #     ["by accident", "on accident"],
    #     ["the subway", "the t", "the metro", "the bart"],
    #     ["soda(s)?", "pop", "coke(s)?", "tonic(s)?", "soft drink(s)?", "cocola(s)?", "fizzy drink(s)?"],
    #     ["carry out", "take out"],
    # ]

    # features_data_path = 'features.csv'
    # features = pd.read_csv(features_data_path)

    # bootstrapping(features, clusters, "confidence_intervals.json")

    # with open("harvard_frequencies.json", 'r') as handle:
    #     freqs = json.load(handle)
    
    # proportions = frequencies_to_proportions(freqs)

    # with open("harvard_proportions.json", "w") as outfile:
    #     json.dump(proportions, outfile, indent = 2)


    # with open("frequencies_clustered.json", 'r') as handle:
    #     freqs = json.load(handle)

    # realtor
    format_table("yelp_proportions.json", "confidence_intervals.json", "harvard_proportions.json", 
                "1", ["realtor(s)?", "estate agent(s)?"],
                "realtors.txt")
    
    # second person
    format_table("yelp_proportions.json", "confidence_intervals.json", "harvard_proportions.json", 
                "4", ["you all", "(yous)|(youse)", "yins", "you lot", "you guys", "you uns", "y all"],
                "second_purpose.txt")
    
    # sandwich
    format_table("yelp_proportions.json", "confidence_intervals.json", "harvard_proportions.json", 
                "7", ["sub(s)?", "hoagie(s)?", "po[or]? boy(s)?", "Italian sandwich(es)?", "sarney(s)?"],
                "sandwiches.txt")
    
    # crawfish
    format_table("yelp_proportions.json", "confidence_intervals.json", "harvard_proportions.json", 
                "9", ["craw fish(es)?", "cray fish(es)?", "craw dad(s)?"],
                "crawfish.txt")

    # grandmother table
    format_table("yelp_proportions.json", "confidence_intervals.json", "harvard_proportions.json", 
                 "11", ["grand mother(s)?", "grann[y|ie](s)?", "grandma(s)?", "nana(s)?", "gramm[y|i|ies](s)?", "gramma(s)?"],
                 "grandmother.txt")
    
    # shoes
    format_table("yelp_proportions.json", "confidence_intervals.json", "harvard_proportions.json", 
                 "14", ["sneaker(s)?", "gym shoe(s)?", "sand shoe(s)?", "jumper(s)?", "tennis shoe(s)?", "running shoe(s)?"],
                 "shoes.txt")
    
    # slaw
    format_table("yelp_proportions.json", "confidence_intervals.json", "harvard_proportions.json", 
                 "25", ["cole slaw", "^(?!cole slaw).*\\bslaw\\b"],
                 "slaw.txt")
    
    # accident
    format_table("yelp_proportions.json", "confidence_intervals.json", "harvard_proportions.json", 
                 "27", ["by accident", "on accident"],
                 "accident.txt")
    
    # trains
    format_table("yelp_proportions.json", "confidence_intervals.json", "harvard_proportions.json", 
                 "31", ["the subway", "the t", "the metro", "the bart"],
                 "trains.txt")
    
    # drinks
    format_table("yelp_proportions.json", "confidence_intervals.json", "harvard_proportions.json", 
                 "32", ["soda(s)?", "pop", "coke(s)?", "tonic(s)?", "soft drink(s)?", "cocola(s)?", "fizzy drink(s)?"],
                 "drinks.txt")

    # togo
    format_table("yelp_proportions.json", "confidence_intervals.json", "harvard_proportions.json", 
                 "36", ["carry out", "take out"],
                 "togo.txt")
