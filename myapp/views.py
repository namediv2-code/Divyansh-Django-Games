import random
from django.shortcuts import render

def home(request):
    result = None
    user_choice = None
    computer_choice = None
    nofg=None
    w=None
    l=None
    t=None

    if "nofg" not in request.session:
        request.session["nofg"]=0
    if "w" not in request.session:
        request.session["w"]=0
    if "l" not in request.session:
        request.session["l"]=0
    if request.POST.get("wish")=="yes":
        request.session["nofg"]=0
        request.session["w"]=0
        request.session["l"]=0
        t=0
    if request.method == 'POST' and request.POST.get("wish")!="yes":
        choices = ['rock', 'paper', 'scissors']
        user_choice = request.POST.get('choice')
        computer_choice = random.choice(choices)
        request.session["nofg"]+=1

        if user_choice == computer_choice:
            result = "It's a tie!"
        elif (
            (user_choice == 'rock' and computer_choice == 'scissors') or
            (user_choice == 'paper' and computer_choice == 'rock') or
            (user_choice == 'scissors' and computer_choice == 'paper')
        ):
            result = "You win!"
            request.session["w"]+=1
        else:
            result = "Computer wins!"
            request.session["l"]+=1

    context = {
        'result': result,
        'user_choice': user_choice,
        'computer_choice': computer_choice,
        'nofg': request.session["nofg"],
        'w': request.session["w"],
        'l': request.session["l"],
        't': request.session["nofg"]-(request.session["w"]+request.session["l"]),
            }
    return render(request, 'myapp/home.html', context)

def guessno(request):
    result=None
    userchoice=None
    if "number" not in request.session:
        request.session["number"]=random.randint(1,100)
    if "nog" not in request.session:
        request.session["nog"]=0
    if request.POST.get("wish")=="Play again":
        request.session.pop("nog",None)
        request.session["nog"]=0
        request.session.pop("number",None)
    if request.method=="POST" and request.POST.get("wish")!="Play again":
        try:
            userchoice=int(request.POST.get("guess"))
            if userchoice<1 or userchoice>100:
                result="Please enter a number from 1 to 100!"
            else:
                request.session["nog"]+=1
                if request.session["nog"]<8:
                    if userchoice<request.session["number"]:
                        result=("Too low. "+str(7-(request.session["nog"]))+" guesses remaining")
                    elif userchoice>request.session["number"]:
                        result=("Too high. "+str(7-(request.session["nog"]))+" guesses remaining")
                    else:
                        result=("Correct!You did it in "+str(request.session["nog"])+" guesses")
                else:
                    result=("Sorry!Ran out of guesses.The number was "+str(request.session["number"]))
        except(ValueError,TypeError):
            result="Please enter a number"
            userchoice=None
    context={"result":result}
    return render(request, 'myapp/guess.html',context) 
def navigation(request):
    return render(request,'myapp/navigation.html',{})
def cricket(request):
    again=None
    decision=None
    bowl=None
    bat=None
    unumber=None
    cnumber=None
    result=None
    showbut=(request.method=="GET")
    if request.POST.get("wish")=="again":
        again=True
        decision=None
        bowl=None
        bat=None
        unumber=None
        cnumber=None
        result=None
        request.session["urun"]=0
        request.session["crun"]=0
        request.session["inning"]=0
        request.session.pop("mode",None)
        request.session["ubowls"]=0
        request.session["cbowls"]=0
    if "inning" not in request.session:
        request.session["inning"]=0
    if "ubowls" not in request.session:
        request.session["ubowls"]=0
    if "cbowls" not in request.session:
        request.session["cbowls"]=0
    if request.method=="POST" and request.POST.get("wish")!="again":
        if request.POST.get("choice")=="bowl":
            request.session["mode"]="bowl"
        elif request.POST.get("choice")=="bat":
            request.session["mode"]="bat"
        mode=request.session["mode"]
        if mode=="bowl":
            if "crun" not in request.session:
                request.session["crun"]=0
            while cnumber==5 or cnumber==None:
                cnumber=random.randint(1,6)
            try:
                unumber=int(request.POST.get("unumber"))
                if unumber<1 or unumber>6 or unumber==5:
                    result="Please enter a number from 1 to 6!"
                else:
                    if unumber==cnumber or request.session["ubowls"]==12:
                        result="Computer is out at "+str(request.session["crun"])+".Out in "+str(1+(request.session["ubowls"]))+" bowls. "+str(request.session["crun"]+1)+" to win!"
                        request.session["inning"]+=1
                        if request.session["inning"]==1:
                            request.session["mode"]="bat"
                        else:
                            request.session["mode"]="done"
                    else:
                        request.session["ubowls"]+=1
                        request.session["crun"]+=cnumber
                        result="Computer keeps playing. Runs are "+str(request.session["crun"])+" "+str(12-(request.session["ubowls"]))+" left"
            except(ValueError,TypeError):
                result="Please enter a valid number"
                unumber=None
        if mode=="bat":
            if "urun" not in request.session:
                request.session["urun"]=0
            cnumber=random.randint(1,20)
            if cnumber==1:
                cnumber=1
            elif 2<=cnumber<=3:
                cnumber=2
            elif 4<=cnumber<=6:
                cnumber=3
            elif 7<=cnumber<=11:
                cnumber=4
            elif 12<=cnumber<=20:
                cnumber=6
            try:
                unumber=int(request.POST.get("unumber"))
                if unumber<1 or unumber>6 or unumber==5:
                    result="Please enter a number from 1 to 6!"
                else:
                    if unumber==1:
                        a=random.randint(1,12)
                        if a==5:
                            unumber=a
                    if unumber==4:
                        a=random.randint(1,5)
                        if a==1:
                            unumber=a
                        elif a==2:
                            unumber=a
                        else:
                            unumber=4
                    if request.session["cbowls"]==12 or cnumber==unumber:
                        result="You are OUT.Your score was "+str(request.session["urun"])+" in "+str(1+(request.session["cbowls"]))+" bowls."
                        request.session["inning"]+=1
                        if request.session["inning"]==1:
                            request.session["mode"]="bowl"
                        else:
                            request.session["mode"]="done"
                        if request.session["cbowls"]<12:
                            pass
                        else:
                            request.session["mode"]="done"
                    else:
                        request.session["cbowls"]+=1
                        request.session["urun"]+=unumber
                        result="Not out!Your score is "+str(request.session["urun"])+" in"+str(request.session["cbowls"])+" bowls."
            except(ValueError,TypeError):
                result="Please enter a valid value!"
                unumber=None
        mode=request.session["mode"]
        bowl=(mode=="bowl")
        bat=(mode=="bat")
        if request.session["mode"]=="done":
            if request.session["crun"]>request.session["urun"]:
                decision="Computer wins!Your score was "+str(request.session["urun"])+" in "+str(request.session["cbowls"])+" bowls. "+" and computer's score was "+str(request.session["crun"])+" in "+str(request.session["ubowls"])+" bowls."
            elif request.session["urun"]>request.session["crun"]:
                decision="You win!Your score was "+str(request.session["urun"])+" in "+str(request.session["cbowls"])+" bowls. "+" and computer's score was "+str(request.session["crun"])+" in "+str(request.session["ubowls"])+" bowls."
            elif request.session["urun"]==request.session["crun"]:
                decision="It's a tie.Your score was "+str(request.session["urun"])+" in "+str(request.session["cbowls"])+" bowls. "+" and computer's score was "+str(request.session["crun"])+" in "+str(request.session["ubowls"])+" bowls."
    context={"showbut":showbut,"again":again,"result":result,"decision":decision,"bowl":bowl,"bat":bat}
    return render(request,'myapp/cricket.html',context)
def crules(request):
    return render(request,'myapp/cricketrules.html',{})