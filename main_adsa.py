class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Minimum degree
        self.leaf = leaf  # True if leaf node
        self.keys = []  # List of keys
        self.children = []  # List of child pointers

    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(None)
            while i >= 0 and self.keys[i] > key:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            while i >= 0 and self.keys[i] > key:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i)
                if self.keys[i] < key:
                    i += 1
            self.children[i].insert_non_full(key)

    def split_child(self, i):
        y = self.children[i]
        z = BTreeNode(y.t, y.leaf)
        self.children.insert(i + 1, z)
        self.keys.insert(i, y.keys[self.t - 1])

        z.keys = y.keys[self.t:(2 * self.t - 1)]
        y.keys = y.keys[0:(self.t - 1)]

        if not y.leaf:
            z.children = y.children[self.t:(2 * self.t)]
            y.children = y.children[0:self.t]

    def remove(self, key):
        idx = self.find_key(key)
        if idx < len(self.keys) and self.keys[idx] == key:
            if self.leaf:
                self.remove_from_leaf(idx)
            else:
                self.remove_from_non_leaf(idx)
        else:
            if self.leaf:
                print(f"The key {key} is not in the tree.")
                return
            flag = (idx == len(self.keys))
            if len(self.children[idx].keys) < self.t:
                self.fill(idx)
            if flag and idx > len(self.keys):
                self.children[idx - 1].remove(key)
            else:
                self.children[idx].remove(key)

    def find_key(self, key):
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < key:
            idx += 1
        return idx

    def remove_from_leaf(self, idx):
        self.keys.pop(idx)

    def remove_from_non_leaf(self, idx):
        key = self.keys[idx]
        if len(self.children[idx].keys) >= self.t:
            pred = self.get_pred(idx)
            self.keys[idx] = pred
            self.children[idx].remove(pred)
        elif len(self.children[idx + 1].keys) >= self.t:
            succ = self.get_succ(idx)
            self.keys[idx] = succ
            self.children[idx + 1].remove(succ)
        else:
            self.merge(idx)
            self.children[idx].remove(key)

    def get_pred(self, idx):
        cur = self.children[idx]
        while not cur.leaf:
            cur = cur.children[len(cur.keys)]
        return cur.keys[len(cur.keys) - 1]

    def get_succ(self, idx):
        cur = self.children[idx + 1]
        while not cur.leaf:
            cur = cur.children[0]
        return cur.keys[0]

    def fill(self, idx):
        if idx != 0 and len(self.children[idx - 1].keys) >= self.t:
            self.borrow_from_prev(idx)
        elif idx != len(self.keys) and len(self.children[idx + 1].keys) >= self.t:
            self.borrow_from_next(idx)
        else:
            if idx != len(self.keys):
                self.merge(idx)
            else:
                self.merge(idx - 1)

    def borrow_from_prev(self, idx):
        child = self.children[idx]
        sibling = self.children[idx - 1]
        child.keys.insert(0, self.keys[idx - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        self.keys[idx - 1] = sibling.keys.pop()

    def borrow_from_next(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]
        child.keys.append(self.keys[idx])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        self.keys[idx] = sibling.keys.pop(0)

    def merge(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]
        child.keys.append(self.keys.pop(idx))
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        self.children.pop(idx + 1)

    def display_level_order(self, level=0, levels=None):
        if levels is None:
            levels = []
        if level == len(levels):
            levels.append([])

        levels[level].append(self.keys)

        for child in self.children:
            child.display_level_order(level + 1, levels)

        return levels

class BTree:
    def __init__(self, t):
        self.root = None
        self.t = t

    def insert(self, key):
        if self.root is None:
            self.root = BTreeNode(self.t, True)
            self.root.keys.append(key)
        else:
            if len(self.root.keys) == 2 * self.t - 1:
                s = BTreeNode(self.t, False)
                s.children.append(self.root)
                s.split_child(0)
                i = 0
                if s.keys[0] < key:
                    i += 1
                s.children[i].insert_non_full(key)
                self.root = s
            else:
                self.root.insert_non_full(key)

    def remove(self, key):
        if not self.root:
            print("The tree is empty")
            return
        self.root.remove(key)
        if len(self.root.keys) == 0:
            tmp = self.root
            if self.root.leaf:
                self.root = None
            else:
                self.root = self.root.children[0]
            del tmp

    def display_level_order(self):
        levels = self.root.display_level_order()
        for i, level in enumerate(levels):
            print(f"Level {i}: ", end="")
            for keys in level:
                print(f"{' '.join(map(str, keys))} | ", end="")
            print()

# Example usage:
degree = int(input("Enter degree of B-Tree:"))
print("Max_Keys = 2 * degree - 1 = ", 2*degree-1 )
btree = BTree(degree)




while True:
        print("\nMenu:")
        print("1. Insert Element")
        print("2. Remove Element")
        print("3. Display Tree")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                key = input("Enter element to insert (or 'q' to quit): ")
                if key.lower() == 'q':
                    break
                btree.insert(key)
        
        elif choice == '2':
            while True:
                key = input("Enter element to remove (or 'q' to quit): ")
                if key.lower() == 'q':
                    break
                btree.remove(key)

        elif choice == '3':
            print("View of tree:")
            btree.display_level_order()
        
        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice! Please try again.")









