#!$HOME/.local/bin/python3
''' this python script generates a netsh script (windows) that restricts the remote ips
    to private network addresses for all firewall rules that match user's selection criterion.
'''
import os

def initialization(fwRulesFile=os.environ['HOME'] + '/repo/intro_to_programming/writing_a_script_with_a_script_fw/fwrules.txt'):
    ''' this subroutine takes as input a stringified path to the file generated by:
        netsh advfirewall firewall show rule all
    '''
    ##### the next two assignment statements hold the start and end of the netsh command to modify firewall rules
    netshLineStart = 'netsh advfirewall firewall set rule name='
    netshLineEnd = ' new remoteip=10.0.0.0/255.0.0.0,172.16.0.0/255.240.0.0,192.168.0.0/255.255.0.0'
    # ^^^ private networks

    return fwRulesFile, netshLineStart, netshLineEnd
    
def make_fwRuleDictionary(fwRulesFile):
    ''' instruct the machine to parse the fwrules.txt file
        and use its contents to build a dictionary-of-dictionaries.
        
        sample record in file:
        Rule Name:                            Virtual Machine Monitoring (Echo Request - ICMPv6-In)
        ----------------------------------------------------------------------
        Enabled:                              No
        Direction:                            In
        Profiles:                             Domain,Private,Public
        Grouping:                             Virtual Machine Monitoring
        LocalIP:                              Any
        RemoteIP:                             Any
        Protocol:                             ICMPv6
                                              Type    Code
                                              Any     Any 
        Edge traversal:                       No
        Action:                               Allow
        
        the keys of the outer dictionary are the rule names,
        and the attributes/settings of a record are the key/value pairs
        of the inner dictionary
    '''
    # build the fwRuleDictionary
    with open(fwRulesFile, 'r') as inFile:
        LoS = inFile.read().splitlines()
        fwRuleDict = dict()
        for line in LoS:
            if 'Rule Name' in line:
                # get rule name & make new instance of attrDict
                ruleName = line.split(':')[-1].strip()
                attrDict = dict()
            if line:
                if 'Rule Name' not in line and '---------' not in line:
                    if ':' in line:
                        attr, colon, value = line.partition(':') #this method is similar to .split(),
                        # except it splits only along the first piece of punctuation in the line.
                        # we use it because some values contain colons, meaning we can't .split()
                        # those lines into key, value pairs
                        attr, value = attr.strip(), value.strip()
                    else:
                        continue
                    attrDict[attr] = value
            if not line: # empty string/empty line
               fwRuleDict[ruleName] = attrDict
    # build the fwRuleDictionary
    return fwRuleDict

def write_output_script(fwRuleDict, netshLineStart, netshLineEnd):
    # sample queries that generate a windows scripts which, when run, modify the rules that match.
    # in this example, we restrict access to all fw rules whose direction is 'In' (inbound) to private networks
#    with open('netsh.cmd', 'w') as outFile:
#        for key, value in fwRuleDict.items():
#            if value['Direction'] == 'In':
#                outFile.write(netshLineStart + '"' + key + '"' + netshLineEnd + "\n")
            
    # in this example, we restrict access to all fw rules with 'RPC' in the key (Rule Name)
    with open('netsh_sbr.cmd', 'w') as outFile:
        for key, value in fwRuleDict.items():
            if 'RPC' in key:
                outFile.write(netshLineStart + '"' + key + '"' + netshLineEnd + "\n")

# set start & end strings of netsh statements;
# get path to file generated by: netsh advfirewall firewall show rule all           
initTuple = initialization()
# read contents of file into session memory as DoD
fwRuleDict = make_fwRuleDictionary(initTuple[0])
# write out netsh script
write_output_script(fwRuleDict, initTuple[1], initTuple[2])
