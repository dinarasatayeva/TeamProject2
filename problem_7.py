import string
from enigma.rotors.rotor import Rotor
from enigma.plugboard import Plugboard
from enigma.machine import EnigmaMachine
from itertools import permutations


# Keep distinct permutations only, eg. keep A-B, but not B-A
def get_distinct_permutations(alphabet):
    return sorted(list(set(tuple(sorted(p)) for p in permutations(alphabet, 2))))

def get_letter_index(letter) -> int:
    return ord(letter) - ord('A')


def get_letter_from_index(index) -> str:
    return chr(index + ord('A'))

# Returns letter pairs list
def get_plugboard(wiring_map):
    plugboard = []
    for index, letter in enumerate(wiring_map):
        letter1 = string.ascii_uppercase[index]
        letter2 = get_letter_from_index(letter)
        if letter1 != letter2:
            plugboard.append((letter1, letter2))

    plugboard = sorted(list(set(tuple(sorted(p)) for p in plugboard)))

    return plugboard

# Prints letter pairs in key sheet format
def print_plugboard(wiring_map):
    plugboard = get_plugboard(wiring_map)
    print(plugboard)
    plugboard_sequence = ''
    for letters in plugboard:
        plugboard_sequence += letters[0] + letters[1] + " "
    print(plugboard_sequence)

# Finds plugboard settings
def decode_plugboard(machine, plaintext, ciphertext, initial_position):
    pb = machine.plugboard
    max_wiring_map = pb.wiring_map

    # Iterate through wiring map until 10 pairs found
    while len(get_plugboard(max_wiring_map)) <= 10:
        wiring_map = max_wiring_map
        unpaired_letters = string.ascii_uppercase
        # Removing found pairs 
        for index, letter_index in enumerate(wiring_map):
            if index != letter_index:
                unpaired_letters = unpaired_letters.replace(get_letter_from_index(letter_index), '')
        max = 0
        # Try letter permutations of unpaired letters to find common letters in known ciphertext and encrypted known plaintext with permutation added to plugbord settings. 
        # Permutations that result in most number of common letters will be added to plugboard settings
        for value in get_distinct_permutations(unpaired_letters):
            pb.wiring_map = wiring_map.copy()
            pb.wiring_map[get_letter_index(value[0])] = get_letter_index(value[1])
            pb.wiring_map[get_letter_index(value[1])] = get_letter_index(value[0])
            machine.set_display(initial_position)
            ciphertext_pb_test = machine.process_text(plaintext)
            if ciphertext == ciphertext_pb_test:
                return pb.wiring_map
            else:
                common_letters = 0
                for index, letter in enumerate(ciphertext):
                    if letter == ciphertext_pb_test[index]:
                        common_letters += 1
                if max < common_letters:
                    max = common_letters
                    max_wiring_map = pb.wiring_map
            


if __name__ == '__main__':
    rL = Rotor('my rotor1', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ring_setting=0, stepping='Q')
    rM = Rotor('my rotor2', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', ring_setting=5, stepping='V')
    rR = Rotor('my rotor3', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', ring_setting=10, stepping='J')

    reflector = Rotor('my reflector', 'YRUHQSLDPXNGOKMIEBFZCWVJAT')

    pb = Plugboard.from_key_sheet()

    machine = EnigmaMachine([rL, rM, rR], reflector, pb)

    known_ciphertext = "YNLIUNHBNVERXKRBUHZEYMJVEZNRPNWOSV"

    known_plaintext = "ATTACK AT 5PM AT ATLANTIC Z ISLAND"

    wiring_map = decode_plugboard(machine, known_plaintext, known_ciphertext, 'UPS')
    print('Initial Rotor -> UPS')

    if wiring_map is not None:
        print('Plugboard settings:')
        print_plugboard(wiring_map)
    else:
        print("Plugboard settings are not found.")
