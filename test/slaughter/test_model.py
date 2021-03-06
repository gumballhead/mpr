from mpr.slaughter.model import parse_record


def test_objects_are_the_same():
    first = parse_record({
        'slug': 'LM_HG201',
        'for_date_begin': '02/01/2019',
        'report_date': '02/02/2018',
        'purchase_type': 'Prod. Sold Negotiated',
        'head_count': '12,771'
    })

    second = parse_record({
        'slug': 'LM_HG201',
        'for_date_begin': '02/01/2019',
        'report_date': '02/02/2018',
        'purchase_type': 'Prod. Sold Negotiated',
        'head_count': '0'
    })

    assert hash(first) == hash(second)


def test_objects_are_not_the_same():
    first = parse_record({
        'slug': 'LM_HG201',
        'for_date_begin': '01/03/2018',
        'report_date': '01/04/2018',
        'purchase_type': 'Prod. Sold Negotiated Formula',
        'head_count': '0'
    })

    second = parse_record({
        'slug': 'LM_HG201',
        'for_date_begin': '01/02/2018',
        'report_date': '01/03/2018',
        'purchase_type': 'Prod. Sold Negotiated Formula',
        'head_count': '0'
    })

    assert hash(first) != hash(second)


def test_contents_are_the_same():
    first = parse_record({
        'slug': 'LM_HG201',
        'for_date_begin': '02/01/2019',
        'report_date': '02/02/2018',
        'purchase_type': 'Prod. Sold Negotiated',
        'head_count': '12,771',
        'base_price': '51.80',
        'avg_net_price': '53.26',
        'lowest_net_price': '43.57',
        'highest_net_price': '57.85',
        'avg_live_weight': '273.54',
        'avg_carcass_weight': '205.41',
        'avg_sort_loss': '-2.16',
        'avg_lean_percent': '55.60',
        'avg_backfat': '.61',
        'avg_loin_depth': '2.61',
        'loineye_area': '7.83'
    })

    second = parse_record({
        'slug': 'LM_HG201',
        'for_date_begin': '02/01/2019',
        'report_date': '02/02/2018',
        'purchase_type': 'Prod. Sold Negotiated',
        'head_count': '12,771',
        'base_price': '51.80',
        'avg_net_price': '53.26',
        'lowest_net_price': '43.57',
        'highest_net_price': '57.85',
        'avg_live_weight': '273.54',
        'avg_carcass_weight': '205.41',
        'avg_sort_loss': '-2.16',
        'avg_lean_percent': '55.60',
        'avg_backfat': '.61',
        'avg_loin_depth': '2.61',
        'loineye_area': '7.83'
    })

    assert first == second


def test_contents_are_not_the_same():
    first = parse_record({
        'slug': 'LM_HG201',
        'for_date_begin': '02/01/2019',
        'report_date': '02/02/2018',
        'purchase_type': 'Prod. Sold Negotiated',
        'head_count': '12,771',
        'base_price': '51.80',
        'avg_net_price': '53.26',
        'lowest_net_price': '43.57',
        'highest_net_price': '57.85',
        'avg_live_weight': '273.54',
        'avg_carcass_weight': '205.41',
        'avg_sort_loss': '-2.16',
        'avg_lean_percent': '55.60',
        'avg_backfat': '.61',
        'avg_loin_depth': '2.61',
        'loineye_area': '7.83'
    })

    second = parse_record({
        'slug': 'LM_HG201',
        'for_date_begin': '02/01/2018',
        'report_date': '02/02/2018',
        'purchase_type': 'Prod. Sold Negotiated',
        'head_count': '0'
    })

    assert first != second
