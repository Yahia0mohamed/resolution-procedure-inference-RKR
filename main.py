import nltk as nl
import regex as reg

IMPLECATION='\u21D2'
FOR_ALL='\u2200'
THERE_EXIST='\u2203'
NOT='\u00AC'
AND='∧'
OR='V'



def changingPropositionFormat(str):
    # we deconstruct the string into tokens so we can do indvidual proposition parsing and changing it
    prop = nl.word_tokenize(str)
    propositions = []
    propTemp = ""
    i = 0
    while i < len(prop):
        if prop[i]==AND or prop[i]==OR:
            propositions.append(propTemp)
            propTemp=""
            propositions.append(prop[i])
            prop = prop[i:]
            i = 0
        elif i>=len(prop)-1:
            propTemp += prop[i]
            propositions.append(propTemp)
        else:
            propTemp += prop[i]
        i += 1
    # reconstructing the proposition
    str=""
    for i in propositions:
        str+= i + " "
    print(str)
    return str

def eliminateImplication(str):
    propositions=str.split(" ")
    # regex part where we search for all the implication phrases and we remove the implication
    regRule = reg.compile(rf'{IMPLECATION}')
    modifiedProp=[]
    for proposition in propositions:
        removed_implication_proposition=""
        if regRule.findall(proposition):
            matches = [(m.group(), m.start()) for m in reg.finditer(regRule, proposition)]
            for match , index in matches:
                removed_implication_proposition=""
                removed_implication_proposition+=NOT + proposition[1:index] + OR + proposition[index + len(match):len(proposition)-1]
                modifiedProp.append(removed_implication_proposition)
        else:
            modifiedProp.append(proposition)
    # reconstructing the proposition
    removed_implication_proposition=""
    for i in modifiedProp:
        removed_implication_proposition+=i +" "
    return removed_implication_proposition



def removeDoubleNot(str):
    # we deconstruct the string into tokens so we can do indvidual proposition parsing and changing it
    propositions=str.split(" ")
    prop=[]
    regRule= reg.compile(rf'{NOT}{NOT}')
    # regex part where we search for all the double not phrases and we remove the it
    for proposition in propositions:
        if regRule.findall(proposition):
            matches = [(m.group(), m.start()) for m in reg.finditer(regRule, proposition)]
            propTemp=""
            for match, index in matches:
                propTemp+=proposition[index + len(match):]
                prop.append(propTemp)
                propTemp=""
        else:
            prop.append(proposition)
    # reconstructing the proposition
    removed_double_not_proposition=""
    for i in prop:
        removed_double_not_proposition+=i +" "
    return removed_double_not_proposition


def deMorganLaw(str):
    propositions=str.split(" ")
    prop=[]
    regRule=reg.compile(rf'{NOT}\([{FOR_ALL}{THERE_EXIST}]+')
    for proposition in propositions:
        if regRule.findall(proposition):
            matches = [(m.group(), m.start()) for m in reg.finditer(regRule, proposition)]
            propTemp=""
            for match, index in matches:
                if match == NOT+'('+FOR_ALL:
                    propTemp+='('+ THERE_EXIST +proposition[3]+ NOT +proposition[index+len(match)+1:]
                    prop.append(propTemp)
                    propTemp=""
                else:
                    propTemp+='('+ FOR_ALL +proposition[3]+ NOT +proposition[index+len(match)+1:]
                    prop.append(propTemp)
                    propTemp=""
        else:
            prop.append(proposition)
    deMorgan_proposition=""
    for i in prop:
        deMorgan_proposition+=i +" "
    return deMorgan_proposition


def standardizeVariableScope(str):
    propositions = str.split(" ")
    propositions = list(filter(None, propositions))
    props = []
    # Find the normal variable
    normal = propositions[0]
    normal_var = next((char for char in normal if char.isalpha()), None)
    current_char='y'
    props.append(propositions[0])
    if normal_var:
        # Iterate over a copy of propositions to avoid modifying it while iterating
        for prop in propositions[1:]:
            if prop in [AND, OR]:
                props.append(prop)
                continue
            for i, char in enumerate(prop):
                if char == normal_var:
                    prop = prop[:i] + current_char + prop[i + 1:]
            props.append(prop)
            current_char=chr(ord(current_char) + 1)
    standardizeVariable_proposition=""
    for i in props:
        standardizeVariable_proposition+=i +" "
    return standardizeVariable_proposition

def prenex_form(str):
    propositions=str.split(" ")
    propositions = list(filter(None, propositions))
    regRule=reg.compile(rf'[{FOR_ALL}{THERE_EXIST}]+[a-z]')
    regRule2 = reg.compile(rf'(?:{NOT})?[a-z]+\([a-z]+\)')

    propTemp=""
    for proposition in propositions:
        if regRule.findall(proposition):
            matches = [(m.group(), m.start()) for m in reg.finditer(regRule, proposition)]
            for match, index in matches:
                propTemp+= match+ " "
    for proposition in propositions:
        if not regRule.findall(proposition) and  not regRule2.findall(proposition):
            propTemp+= proposition +" "
        if regRule2.findall(proposition):
            matches = [(m.group(), m.start()) for m in reg.finditer(regRule2, proposition)]
            for match, index in matches:
                propTemp+= match+ " "

    return propTemp

def skolemization(str):
    propositions = str.split(" ")
    propositions = list(filter(None, propositions))
    curr_char = 'A'
    curr_func = "F"
    prob_temp = ""
    n = len(propositions)
    proposition = 0 

    while proposition < n:

        if propositions[proposition][0] == THERE_EXIST :
            param = propositions[proposition][1]
            propositions.pop(proposition)
            propositions.insert(proposition, "")
            regRule2 = reg.compile(rf'(?:{NOT})?[a-z]+\({param}+\)')
            for i in propositions:
                if regRule2.findall(i):
                    matches = [(m.group(), m.start()) for m in reg.finditer(regRule2, i)]
                    for match, index in matches:
                        index_of_match= propositions.index(match)
                        propositions.pop(index_of_match)
                        if match[0] == NOT:
                            modified_match = match[:3] + curr_char + match[4:]
                        else:
                            modified_match = match[:2] + curr_char + match[3:]
                        propositions.insert(index_of_match, modified_match)

        elif  proposition <= n - 1 and propositions[proposition][0] == FOR_ALL and propositions[proposition+1][0] == THERE_EXIST:
            param = propositions[proposition + 1][1]
            prev_param = propositions[proposition][1]
            propositions.pop(proposition + 1)
            propositions.insert(proposition, "")
            regRule2 = reg.compile(rf'(?:{NOT})?[a-z]+\({param}+\)')
            
            for i in propositions:
                if regRule2.findall(i):
                    matches = [(m.group(), m.start()) for m in reg.finditer(regRule2, i)]
                    for match , index in matches:
                        index_of_match= propositions.index(match)
                        propositions.pop(index_of_match)
                        if match[0] == NOT:
                            modified_match = match[:3] + curr_func+"("+prev_param+")" + match[4:] + " "
                        else:
                            modified_match = match[:2] + curr_func+"("+prev_param+")" + match[3:] + " "
                        propositions.insert(index_of_match, modified_match)

        else:
            prob_temp+=propositions[proposition]
        proposition += 1
        curr_char=chr(ord(curr_char) + 1)
        
    propositions = list(filter(None, propositions))
    prob_temp = "" 
    for i in propositions:
        prob_temp += i + " "

    return prob_temp

    # ∀x P( x) ∨ Q(F ( x)) → P( x) ∨ Q(F ( x))
def eliminateUniversalQuantifiers(str):
    propositions = str.split(" ")
    propositions = list(filter(None, propositions))
    regRule=reg.compile(rf'[{FOR_ALL}]+[a-z]')
    for i in propositions:
        if regRule.findall(i):
            matches = [(m.group(), m.start()) for m in reg.finditer(regRule, i)]
            for match, index in matches:
                index_of_match= propositions.index(match)
                propositions.pop(index_of_match)
    prob_temp = "" 
    for i in propositions:
        prob_temp += i + " "
    return prob_temp

def CNF(str):
    str = changingPropositionFormat(str)
    print(str)
    str = eliminateImplication(str)
    print(str)
    str = removeDoubleNot(str)
    print(str)
    str = deMorganLaw(str)
    print(str)
    str = standardizeVariableScope(str)
    print(str)
    str = prenex_form(str)
    print(str)
    str = skolemization(str)
    print(str)
    str = eliminateUniversalQuantifiers(str)
    return str






def main():
    predicate=f"{NOT}({FOR_ALL}x p(x)) {AND} {NOT}({THERE_EXIST}x p(x)) {OR} {NOT}({FOR_ALL}x p(x))"
    print(predicate)
    print(CNF(predicate))



if __name__ == "__main__":
    main()