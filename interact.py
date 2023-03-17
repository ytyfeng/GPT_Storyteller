
interact = True

while (interact):
    print("Interests: l, Facets: f, Affinity Rules: r, Instance: i, Exit e")
    selector = input("Select an option: ")
    match selector:
        case 'l':
            print("Enter interest:")
        case 'f':
            print("Enter facet:")
        case 'r':
            print("Enter Affinity Rule:")
        case 'i':
            print("instance stuff")
            instance_bool = True
            while (instance_bool):
                print("Create character: c, Set facet level: f, Set interest level: i, Pair facet similarity: p, Match attribute levels: m, Exit: e")
                selector_instance = input("Select a type of instance to create:")
                match selector_instance:
                    case 'c':
                        name = input("Name a character:")
                        print("character(" + name + ").")
                    case other:
                        instance_bool = False
        case 'e':
            intract = False
        case other:
            print("Invalid input.")