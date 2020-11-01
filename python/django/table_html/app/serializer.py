from .models import Computer, info



from rest_framework import serializers






class computerSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Computer
        fields = ['id','name','number','n_type','unit','unit_price','quantity','note','info']

#
#
#
# class infoS(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = info


class infoSerializers(serializers.HyperlinkedModelSerializer):
    # com = serializers.CharField(source='Computer.id')
    # info = infoS()
    class Meta:
        model = info
        fields = ['cpu','hard_disk','video_memory','memory']

