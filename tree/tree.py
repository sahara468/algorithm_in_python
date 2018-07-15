class TreeNode(object):
    def __init__(self, treenode_val, treenode_type):
        self.value = treenode_val
        self.type = treenode_type
        self.parent_node = None
        self.children_nodes = []
        self.is_leaf_node = True

    def add_child(self, child_node):
        self.is_leaf_node = False
        self.children_nodes.append(child_node)
        assert isinstance(child_node, TreeNode)
        child_node.parent_node = self

    def treenode_to_str_detail(self, indent=4):
        ret_str = ""
        if not self.children_nodes:
            ret_str += " " * indent + "type=%s, " % str(self.type) + \
                "\n" + " " * indent + "value=%s, " % str(self.value) + \
                "\n" + " " * indent + "children_nodes: null"
            return ret_str
        else:
            ret_str += " " * indent + "type=%s, " % str(self.type) + \
                "\n" + " " * indent + "value=%s, " % str(self.value) + \
                "\n" + " " * indent + "children_nodes: \n"
            for child in self.children_nodes:
                child_str = child.treenode_to_str_detail(indent)
                temp_str = ""
                for s in child_str.split("\n"):
                    if s:
                        temp_str += " " * indent + s + "\n"
                ret_str += temp_str
                ret_str += "\n"
            return ret_str

    def treenode_to_str(self, indent=4):
        ret_str = ""
        if not self.children_nodes:
            ret_str += " " * indent + str(self.value)
            return ret_str
        else:
            ret_str += " " * indent + str(self.value) + " " * indent + "\n"
            for child in self.children_nodes:
                child_str = child.treenode_to_str(indent)
                temp_str = ""
                for s in child_str.split("\n"):
                    if s:
                        temp_str += " " * indent + s + "\n"
                ret_str += temp_str
            return ret_str

    def to_csv(self):
        if hasattr(self.value, "to_csv"):
            val_csv = self.value.to_csv()
        else:
            val_csv = str(self.value)
        return val_csv


class Tree(object):
    def __init__(self, root_node):
        self.root_node = root_node

    def get_tree_height(self):
        height = 0
        if not self.root_node:
            return 0
        else:
            height += 1
            children_nodes_height = []
            for child in self.root_node.children_nodes:
                children_nodes_height.append(Tree(child).get_tree_height())
            if children_nodes_height:
                height += max(children_nodes_height)
            return height

    def get_tree_leaf_nodes(self):
        leaf_nodes = []
        if not self.root_node:
            return []
        queue = [self.root_node]
        while len(queue):
            node = queue.pop()
            if node.is_leaf_node:
                leaf_nodes.append(node)
            for child in node.children_nodes:
                if len(child.children_nodes):
                    queue.append(child)
                else:
                    if child.is_leaf_node:
                        leaf_nodes.append(child)
        return leaf_nodes

    def print_tree(self, detail=False, indent=4):
        if detail:
            print self.root_node.treenode_to_str_detail(indent)
        else:
            print self.root_node.treenode_to_str(indent)

    def tree_to_csv(self):
        leaf_nodes = self.get_tree_leaf_nodes()
        tree_height = self.get_tree_height()
        csv_content = ""
        for leaf_node in leaf_nodes:
            leaf_line = ""
            current_node = leaf_node
            leaf_height = 1
            while current_node.parent_node is not None:
                leaf_height += 1
                leaf_line = "%s,%s" % (current_node.to_csv(), leaf_line)
                current_node = current_node.parent_node
            leaf_line = "%s,%s" % (current_node.to_csv(), leaf_line)
            if leaf_height < tree_height:
                leaf_line = "%s%s" % (leaf_line, "," * (tree_height - leaf_height))
            csv_content += "%s\n" % leaf_line
        return csv_content


class Student(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


if __name__ == "__main__":
    #     Tree Example
    #             1
    #      /      |       \
    #     5       6        7
    #             |     /  |  \
    #           zhang  8   9   10
    #           /   \
    #         yang  100
    root_treenode = TreeNode(1, int)
    child_node1 = TreeNode(5, int)
    child_node2 = TreeNode(6, int)
    child_node3 = TreeNode(7, int)

    root_treenode.add_child(child_node1)
    root_treenode.add_child(child_node2)
    root_treenode.add_child(child_node3)

    child_node4 = TreeNode(Student("zhang"), Student)
    child_node2.add_child(child_node4)

    child_node5 = TreeNode(Student("yang"), Student)
    child_node6 = TreeNode(100, int)

    child_node4.add_child(child_node5)
    child_node4.add_child(child_node6)

    child_node7 = TreeNode(8, int)
    child_node8 = TreeNode(9, int)
    child_node9 = TreeNode(10, int)

    child_node3.add_child(child_node7)
    child_node3.add_child(child_node8)
    child_node3.add_child(child_node9)

    tree = Tree(root_treenode)
    print tree.tree_to_csv()

    tree.print_tree()
