from collections import defaultdict, Counter
import pandas as pd
import json
from matplotlib import pyplot as plt

word_clusters = [
    ["mischievous", "mischievious"],
    ["realtor(s)?", "estate agent(s)?"],
    ["spigot(s)?", "spicket(s)?"],
    ["dragged", "drug"],
    ["you all", "(yous)|(youse)", "yins", "you lot", "you guys", "you uns", "y all"],
    ["tag sale(s)?", "yard sale(s)?", "garage sale(s)?", "rummage sale(s)?", "thrift sale(s)?", "stoop sale(s)?", "car port sale(s)?", "side walk sale(s)?", "jumble sale(s)?", "car boot sale(s)?", "patio sale(s)?"],
    ["mumblety peg(s)?", "mumbledy peg(s)?", "mumbly peg(s)?", "mumblely peg(s)?", "mumble peg(s)?", "mummety peg(s)?", "numblety peg(s)?", "base ball jack knife", "stick knife", "stick frog(s)?", "stretch", "knifey", "splits"],
    ["sub(s)?", "grinder(s)?", "hoagie(s)?", "po[or]? boy(s)?", "Italian sandwich(es)?", "sarney(s)?"],
    ["fire fl(y|ies)", "lightning bug(s)?"],
    ["craw fish(es)?", "cray fish(es)?", "craw dad(s)?"],
    ["daddy long leg(s)?", "daddy big leg(s)?", "daddy bug(s)?", "father long leg(s)?", "daddy gray beard(s)?", "harvest man", "moskeet spider(s)?"],
    ["grand mother(s)?", "granny(s)?", "grandma(s)?", "nana(s)?", "gramm[y|i](s)?", "gramma(s)?"],
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
    ["the subway", "(the l)|(the el)", "the t", "the metro", "the bart"],
    ["soda(s)?", "pop", "coke(s)?", "tonic(s)?", "soft drink(s)?", "cocola(s)?", "fizzy drink(s)?"],
    ["gate night(s)?", "trick night(s)?", "mischief night(s)?", "cabbage night(s)?", "goosey night(s)?", "devil s night(s)?", "devil s eve(s)?"],
    ["moot point(s)?", "mute point(s)?"],
    ["brew thru(s)?", "party barn(s)?", "boot legger(s)?", "beer barn(s)?", "beverage barn(s)?"],
    ["carry out", "take out"],
    ["ogl[e|es|ed|ing]", "oogl[e|es|ed|ing]", "oggl[e|es|ed|ing]"],
    ["modals"],
]

def count_regional_frequencies(features):

    regional_frequencies = defaultdict(lambda : defaultdict(lambda: defaultdict(lambda: 0)))
    
    for i in range(features.shape[0]):
    # for i in range(10):
        state = features["state"][i]
        for cluster_index, cluster in enumerate(word_clusters):
            for word in cluster:
                regional_frequencies[cluster_index][state][word] += int(features[word][i])
        if i % 1000 == 0: print(i)
    return regional_frequencies

if __name__ == '__main__':
    features = pd.read_csv("features.csv")

    state_frequency = features["state"].value_counts()

    missing_features = []
    feat_counts = {}
    for f in features.columns:
        if f != "state":
            if features[f].sum() == 0:
                missing_features.append(f)
            feat_counts[f] = features[f].sum()
    
    # print(feat_counts)

    print("missing features: ", len(missing_features))

    regional_frequencies = count_regional_frequencies(features)

    with open("frequencies.json", "w") as outfile:
        json.dump(regional_frequencies, outfile, indent = 2)

    # with open('frequencies.json', 'r') as handle:
    #     regional_frequencies = json.load(handle)
    
    # for cluster_num in regional_frequencies:
    #     for state in regional_frequencies[cluster_num]:
    #         words = []
    #         counts = []
    #         for word in regional_frequencies[cluster_num][state]:
    #             words.append(word)
    #             counts.append(regional_frequencies[cluster_num][state][word])
    #         plt.pie(counts, labels = words, autopct='%1.0f%%')
    #         plt.savefig("plots/plot_" + str(cluster_num) + "_" + state + ".png")

    # print(regional_frequencies)
