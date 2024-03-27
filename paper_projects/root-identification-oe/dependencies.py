from token import get_from_id


def trigger(rule_root, isolated):
    # Check if the string is a valid function name
    if not callable(rule_root):
        raise ValueError(f"Invalid function name {rule_root}")

    res = rule_root(isolated)
    return res


def vb(isolated):
    if len(isolated) == 1:
        potential_root = isolated[0]
        if '+' in potential_root.tag:
            tag = potential_root.tag.split('+')[1].strip()
        else:
            tag = potential_root.tag
        if tag.startswith('VB'):
            potential_root.add_attrs(deprel='root')
            return True
        return False
    else:
        iso_vbs = [tok for tok in isolated if tok.tag.startswith('VB') or tok.tag.startswith('RP+VB') or tok.tag.startswith('NEG+VB')]
        if len(iso_vbs) == 1:
            root = iso_vbs[0]
            root.add_attrs(deprel='root')
            for tok in isolated:
                if tok.tag.startswith('MD'):
                    tok.add_attrs(deprel='aux', head=id(root))
                else:
                    pass
            return True
        return False


def be_inf(isolated):
    iso_bes = [tok for tok in isolated if tok.tag.startswith('BE')]
    if len(iso_bes) == 1:
        potential_root = iso_bes[0]
        following = potential_root.next_tok()
        if following.tag.startswith('TO'):
            ip_inf = get_from_id(following.parent)
            return ip_inf.infinitive_dep(parent=potential_root)
        return False
    return False


def be_copula(isolated):
    iso_bes = [tok for tok in isolated if tok.tag.startswith('BE')]
    if len(iso_bes) == 1:
        potential_copula = iso_bes[0]
        sentence = get_from_id(potential_copula.parent)
        higher_level = get_from_id(potential_copula.parent)
        same_level_prd = [prd for prd in higher_level if prd.tag.endswith('-NOM-PRD')]
        if len(same_level_prd) == 1:
            root_prd = same_level_prd[0]
            nom_parent = root_prd.get_nom_parent()
            if nom_parent:
                nom_parent.add_attrs(deprel='root')
                potential_copula.add_attrs(deprel='cop', head=id(nom_parent))
                return True
            return False
        return False
    return False


def have(isolated):
    if len(isolated) == 1:
        potential_root = isolated[0]
        if '+' in potential_root.tag:
            tag = potential_root.tag.split('+')[1].strip()
        else:
            tag = potential_root.tag
        if tag.startswith('HV'):
            potential_root.add_attrs(deprel='root')
            return True
        return False
    else:
        iso_vbs = [tok for tok in isolated if tok.tag.startswith('HV') or tok.tag.startswith('RP+HV') or tok.tag.startswith('NEG+HV')]
        if len(iso_vbs) == 1:
            root = iso_vbs[0]
            root.add_attrs(deprel='root')
            for tok in isolated:
                if tok.tag.startswith('MD'):
                    tok.add_attrs(deprel='aux', head=id(root))
                else:
                    pass
            return True
        return False


def be_root(isolated):
    if len(isolated) == 1:
        potential_root = isolated[0]
        if '+' in potential_root.tag:
            tag = potential_root.tag.split('+')[1].strip()
        else:
            tag = potential_root.tag
        if tag.startswith('BE'):
            potential_root.add_attrs(deprel='root')
            return True
        return False
    else:
        iso_vbs = [tok for tok in isolated if tok.tag.startswith('BE') or tok.tag.startswith('NEG+BE')]
        if len(iso_vbs) == 1:
            root = iso_vbs[0]
            root.add_attrs(deprel='root')
            for tok in isolated:
                if tok.tag.startswith('MD'):
                    tok.add_attrs(deprel='aux', head=id(root))
                else:
                    pass
            return True
        elif len(iso_vbs) == 2:
            for be in iso_vbs:
                if be.tag == 'BEN':
                    be.add_attrs(deprel='root')
                    return True
        return False


def md(isolated):
    if len(isolated) == 1:
        potential_root = isolated[0]
        if '+' in potential_root.tag:
            tag = potential_root.tag.split('+')[1].strip()
        else:
            tag = potential_root.tag
        if tag.startswith('MD'):
            potential_root.add_attrs(deprel='root')
            return True
        return False
    else:
        iso_vbs = [tok for tok in isolated if tok.tag.startswith('MD') or tok.tag.startswith('RP+MD') or tok.tag.startswith('NEG+MD')]
        if len(iso_vbs) == 1:
            root = iso_vbs[0]
            root.add_attrs(deprel='root')
            return True
        return False
