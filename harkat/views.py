from django.shortcuts import render
from harkat.models import Harkat

# Create your views here.


def percentage(kol, jozea):
    print("______")
    print("kol:", kol, ", joz:", jozea)
    print("j100", int(jozea) * 100)
    print("j", int(jozea) * 100 / int(kol))
    if kol == 0:
        return 0
    elif kol == jozea:
        return 100
    else:
        return int(jozea) * 100 / int(kol)


# def harekat_main(request):
#     harkat_data = []
#     all_harkat = Harekat.objects.all()
#     for hrkat in all_harkat:
#         mablaghe_jam_shode = hrkat.TotalAmount
#         # @todo: annonate sum
#
#
#         harkat_data.append({
#             'id': hrkat.id,
#             'Title': hrkat.Title,
#             'Slug': hrkat.Slug,
#             'Picture': hrkat.Picture,
#             'TotalAmount': hrkat.TotalAmount,
#             'Amount': hrkat.Amount,
#             'Description': hrkat.Description,
#             'MadadKar': hrkat.MadadKar,
#         })
#
#     return render(request, "harekat.html", context={'harkat': harkat_data})


def harkat_single(request, id):
    harkatdata = Harkat.objects.filter(id=id).get()
    data = {
        "data": harkatdata,
        "percent_amount": int(percentage(harkatdata.Amount, harkatdata.TotalAmount))
    }
    return render(request, "harekat_data.html", context={"data": data})
