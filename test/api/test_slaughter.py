from unittest import TestCase
from datetime import date

from test.api import parse_report
from mpr.data.api.slaughter import parse_attributes

report = """
    <results exportTime="2019-02-11 21:04:13">
        <report label="National Daily Direct Hog Prior Day - Slaughtered Swine" slug="LM_HG201">
            <record report_date="02/04/2019" for_date_begin="02/01/2019">
                <report label="Barrows/Gilts">
                    <record purchase_type="Prod. Sold Negotiated" head_count="12,771" base_price="51.80" avg_net_price="53.26" lowest_net_price="43.57" highest_net_price="57.85" avg_live_weight="273.54" avg_carcass_weight="205.41" avg_sort_loss="-2.16" avg_backfat=".61" avg_loin_depth="2.61" loineye_area="7.83" avg_lean_percent="55.60"/>
                    <record purchase_type="Prod. Sold Other Market Formula" head_count="71,962" base_price="56.81" avg_net_price="59.14" lowest_net_price="47.51" highest_net_price="69.91" avg_live_weight="288.18" avg_carcass_weight="218.50" avg_sort_loss="-2.14" avg_backfat=".61" avg_loin_depth="2.73" loineye_area="8.23" avg_lean_percent="56.29"/>
                    <record purchase_type="Prod. Sold Swine or Pork Market Formula" head_count="256,439" base_price="55.53" avg_net_price="57.65" lowest_net_price="37.89" highest_net_price="67.65" avg_live_weight="286.91" avg_carcass_weight="216.06" avg_sort_loss="-1.85" avg_backfat=".64" avg_loin_depth="2.65" loineye_area="7.97" avg_lean_percent="56.00"/>
                    <record purchase_type="Prod. Sold Other Purchase Arrangement" head_count="134,335" base_price="63.31" avg_net_price="64.15" lowest_net_price="47.39" highest_net_price="77.44" avg_live_weight="284.97" avg_carcass_weight="213.73" avg_sort_loss="-1.51" avg_backfat=".71" avg_loin_depth="2.49" loineye_area="7.48" avg_lean_percent="55.18"/>
                    <record purchase_type="Prod. Sold Negotiated Formula" head_count="683"/>
                    <record purchase_type="Prod. Sold (All Purchase Types)" head_count="476,190" base_price="57.81" avg_net_price="59.63" lowest_net_price="45.13" highest_net_price="71.45" avg_live_weight="286.21" avg_carcass_weight="215.47" avg_sort_loss="-1.81" avg_backfat=".65" avg_loin_depth="2.63" loineye_area="7.91" avg_lean_percent="55.87"/>
                    <record purchase_type="Pack. Sold (All Purchase Types)" head_count="15,214" base_price="53.84" avg_net_price="56.13" lowest_net_price="53.01" highest_net_price="64.42" avg_live_weight="284.25" avg_carcass_weight="210.30" avg_sort_loss="-2.35" avg_backfat=".59" avg_loin_depth="2.64" loineye_area="7.94" avg_lean_percent="55.92"/>
                    <record purchase_type="Packer Owned" head_count="252,211" avg_live_weight="287.07" avg_carcass_weight="218.47" avg_backfat=".67" avg_loin_depth="2.52" loineye_area="7.57" avg_lean_percent="54.11"/>
                </report>
            </record>
        </report>
    </results>
"""

records = list(parse_report(report))
attributes = records[0]
negotiated = parse_attributes(attributes)

class PurchaseTest(TestCase):
    def test_parse_length(self):
        self.assertEqual(len(records), 8)

    def test_date(self):
        self.assertEqual(negotiated.date, date(2019, 2, 1))
    
    def test_purchase_type(self):
        self.assertEqual(negotiated.purchase_type, 'Prod. Sold Negotiated')
    
    def test_head_count(self):
        self.assertEqual(negotiated.head_count, 12771)
    
    def test_base_price(self):
        self.assertEqual(negotiated.base_price, 51.8)
    
    def test_net_price(self):
        self.assertEqual(negotiated.net_price, 53.26)
    
    def test_low_price(self):
        self.assertEqual(negotiated.low_price, 43.57)
    
    def test_high_price(self):
        self.assertEqual(negotiated.high_price, 57.85)
    
    def test_live_weight(self):
        self.assertEqual(negotiated.live_weight, 273.54)
    
    def test_carcass_weight(self):
        self.assertEqual(negotiated.carcass_weight, 205.41)
    
    def test_sort_loss(self):
        self.assertEqual(negotiated.sort_loss, -2.16)

    def test_backfat(self):
        self.assertEqual(negotiated.backfat, 0.61)
    
    def test_loin_depth(self):
        self.assertEqual(negotiated.loin_depth, 2.61)
    
    def test_loineye_area(self):
        self.assertEqual(negotiated.loineye_area, 7.83)
    
    def test_lean_percent(self):
        self.assertEqual(negotiated.lean_percent, 55.6)