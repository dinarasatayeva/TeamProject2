from enigma.rotors.rotor import Rotor
from enigma.plugboard import Plugboard
from enigma.machine import EnigmaMachine

def find_display(machine, ciphertext, known_plaintext): 
    for init_pos_1 in range(26):
        for init_pos_2 in range(26):
            for init_pos_3 in range(26):
                
                machine.set_display("{}{}{}".format(chr(ord('A') + init_pos_1), chr(ord('A') + init_pos_2), chr(ord('A') + init_pos_3)))
                
                if ciphertext == machine.process_text(known_plaintext):
                    return "{}{}{}".format(chr(ord('A') + init_pos_1), chr(ord('A') + init_pos_2), chr(ord('A') + init_pos_3))
                
    return None
            
rL = Rotor('my rotor1', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ring_setting=0, stepping='Q')
rM = Rotor('my rotor2', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', ring_setting=5, stepping='V')
rR = Rotor('my rotor3', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', ring_setting=10, stepping='J')

reflector = Rotor('my reflector', 'YRUHQSLDPXNGOKMIEBFZCWVJAT')

pb = Plugboard.from_key_sheet('AK BZ CG DL FU HJ MX NR OY PW')

machine = EnigmaMachine([rL, rM, rR], reflector, pb)

ciphertext = "WVUVJCSQBFLWSGTHDREWOSXYIAYEUBHHXY"
known_plaintext = "ATTACK AT 5PM AT ATLANTIC Z ISLAND"

result = find_display(machine, ciphertext, known_plaintext)

if result is not None:
    print("Initial rotor positions (display): " + result)
else: 
    print ("Could not recover rotor initial position (display).")
                