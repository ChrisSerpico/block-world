import Parse

Parse.readParseRules("parseRules.dat")

question = "Where is Block1".split(" ")
#question1 = "What is on Block1".split(" ")

Parse.parse(question)
#Parse.parse(question1)

