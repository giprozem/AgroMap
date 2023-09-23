from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
from hub.models import PropertyTypeList, DocumentTypeList, CategoryTypeList, LandTypeList
from hub.models.base import BaseModel


class LandInfo(BaseModel):
    history = HistoricalRecords(verbose_name=_("History"), inherit=True)
    ink_code = models.CharField(max_length=100, verbose_name=_('INK Code'))
    main_map = models.GeometryField(verbose_name=_('Contour'), blank=True, null=True)
    inn_pin = models.IntegerField(blank=True, null=True, verbose_name=_('Tax ID'))
    bonitet = models.IntegerField(blank=True, null=True, verbose_name=_('Bonniness'))
    culture = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Crop Type'))
    crop_yield = models.DecimalField(decimal_places=2, max_digits=100, blank=True, null=True,
                                     verbose_name=_('Crop Yield'))
    property_type = models.ForeignKey(PropertyTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='land_info', verbose_name=_('Property Type'))
    document_type = models.ForeignKey(DocumentTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='land_info', verbose_name=_('Document Type'))
    document_link = models.FileField(upload_to='document', blank=True, null=True, verbose_name=_('Document Link'))
    category_type = models.ForeignKey(CategoryTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='land_info', verbose_name=_('Land Categories'))
    land_type = models.ForeignKey(LandTypeList, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='land_info', verbose_name=_('Land Type Information'))
    square = models.DecimalField(decimal_places=2, max_digits=100, blank=True, null=True,
                                 verbose_name=_('Actual Area'))
    """Zem Balance"""
    longitude = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Longitude'))
    latitude = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Latitude'))
    land_no = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Land Number'))
    territorial_outline = models.CharField(max_length=100, blank=True, null=True,
                                           verbose_name=_('Administrative-Territorial Division'))
    number_realestateunits = models.CharField(max_length=100, blank=True, null=True,
                                              verbose_name=_('Number of Real Estate Units'))
    circuit_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Circuit Number'))
    doc_enttitlement = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Document Entitlement'))
    use_period = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Use Period (Years)'))
    certifying_act = models.CharField(max_length=55, blank=True, null=True,
                                      verbose_name=_('Certifying Act (Attach File)'))
    use_end = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Use End Date'))
    agroland_purposes = models.CharField(max_length=55, blank=True, null=True,
                                         verbose_name=_('Agricultural Land Purposes'))
    gfsu = models.CharField(max_length=255, blank=True, null=True,
                            verbose_name=_('State Fund of Agricultural Lands'))
    lands_pop_areas = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Lands in Populated Areas'))
    othertypes_lands = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Other Types of Lands'))
    type_of_land = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Land Types'))
    agro_type_land = models.CharField(max_length=255, blank=True, null=True,
                                      verbose_name=_('Agricultural Land Type'))
    desc_brd = models.TextField(blank=True, null=True, verbose_name=_('Description of Restrictions'))
    date_of_completion = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Completion Date'))
    perrenial_plant = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Perennial Plants'))
    forest_areas = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Forest Areas'))
    underwater = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Underwater'))
    otherlands = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Other Lands'))
    collective_gardens_and_veg = models.CharField(max_length=255, blank=True, null=True,
                                                  verbose_name=_('Collective Gardens and Vegetable Plots'))
    irrigated = models.CharField(max_length=3, blank=True, null=True, verbose_name=_('Irrigated'))
    rainfed = models.CharField(max_length=3, blank=True, null=True, verbose_name=_('Rainfed'))
    improved_radical = models.CharField(max_length=3, blank=True, null=True,
                                        verbose_name=_('Improved (Radical Improvement)'))
    inaccessible = models.CharField(max_length=3, blank=True, null=True,
                                    verbose_name=_('Inaccessible Due to Difficulty of Access'))
    intensive_use = models.CharField(max_length=3, blank=True, null=True, verbose_name=_('Intensive Use'))
    pasture = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Pasture'))
    plant_not_forestfund = models.CharField(max_length=255, blank=True, null=True,
                                            verbose_name=_('Non-Forest Fund Woody and Shrub Plantations'))
    property_form = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Property Form'))
    disturbed_lands = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Disturbed Lands'))
    lot_number = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Lot Number'))
    elementary_sectionnumber = models.CharField(max_length=55, blank=True, null=True,
                                                verbose_name=_('Elementary Section Number'))

    descriptiom_doc = models.TextField(blank=True, null=True, verbose_name=_('Description (if needed)'))
    udp = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Long-Term Land Use'))
    limite = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Limitations'))

    haushold_land = models.CharField(max_length=55, blank=True, null=True,
                                     verbose_name=_('Household Lands and Citizen Allotments'))
    number_of_yards = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Number of Yards'))
    number_of_families = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Number of Families'))
    total_land = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Total Land'))
    crmid = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Identification Number'))
    smcreatorid = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Creator'))
    smownerid = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Owner'))
    modifiedby = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Modified By'))
    setype = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Type'))
    description = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Description'))
    land_ctg = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Land Categories (Land Balance)'))
    status = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Status'))
    """Kadastr"""
    eni_code = models.CharField(max_length=35, blank=True, null=True, verbose_name=_('ENI Code'))
    asr_address = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Parcel Address (ASR)'))
    special_purpose_asr = models.CharField(max_length=100, blank=True, null=True,
                                           verbose_name=_('Special Purpose (ASR)'))
    land_factarea_asr = models.CharField(max_length=255, blank=True, null=True,
                                         verbose_name=_('Actual Area (ASR)'))
    form_using_asr = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('Use Form (ASR)'))
    land_legalarea = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Legal Area (ASR)'))
    owner_info = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Owner Information (ASR)'))

    class Meta:
        verbose_name = _('Main Table')
        verbose_name_plural = _("Main Table")

    def __str__(self):
        return self.ink_code

