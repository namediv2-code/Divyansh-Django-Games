import random
import time
from django.shortcuts import render
from django.shortcuts import render, redirect
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
def trivia(request):
    q=["1+1?\na.1 b.2 c.3 d.11","2+2?\na.4 b.2 c.12 d.22","1+2?\na.3 b.4 c.2 d.9"]
    a=["b","a","a"]
    if "p" not in request.session:
        request.session["p"]=0
    if "times" not in request.session:
        request.session["times"]=0
    question=None
    result=None
    mode=None
    tim=None
    r=None
    h=None
    if request.POST.get("wish")=="again":
        request.session["p"]=0
        request.session["times"]=0
        request.session.pop("r",None)
        request.session.pop("l",None)
        request.session.pop("s",None)
    elif request.POST.get("start")=="play" and request.session["times"]<5:
        request.session["s"]=random.randint(1,10)
        request.session["l"]=random.randint(0,2)
        request.session["r"]=time.time()
        tim="You have "+str(request.session["s"])+" seconds to answer this question"
        question=q[request.session["l"]]
    elif request.POST.get("option") and request.session["times"]<5:
        h=time.time()
        request.session["times"]+=1
        if request.POST.get("option") == "timeout":
            result = "Time's up!\n+0 points"
        elif request.POST.get("option")==a[request.session["l"]]:
            if h-request.session["r"]>request.session["s"]:
                result="Correct!But you took too long!!!\n+0 points"
            else:
                request.session["p"]+=5+round(request.session["s"]+request.session["r"]-h)
                result="Correct!\n+5 points\n+"+str(round(request.session["s"]-h+request.session["r"]))+" bonus points"
        else:
            result="WRONG\n+0 points"
        if request.session["times"] < 5:
            request.session["s"] = random.randint(1,10)
            request.session["l"] = random.randint(0,2)
            request.session["r"] = time.time()
            tim = "You have "+str(request.session["s"])+" seconds to answer this question"
            question = q[request.session["l"]]
        else:
            request.session.pop("r",None)
            request.session.pop("l",None)
            request.session.pop("s",None)
    elif "l" in request.session and request.session["times"]<5:
        tim="You have "+str(request.session["s"])+" seconds to answer this question"
        question=q[request.session["l"]]
    mode=request.session["times"]<5
    context={"time":tim,"question":question,"result":result,"p":request.session["p"],"mode":mode,"s":request.session.get("s",10)}
    return render(request,'myapp/trivia.html',context)
def computerGuesses(request):
    guesses=None
    guess=None
    mode=None
    g=None
    show=False
    ges=None
    if request.method=="GET":
        show=True
    if request.POST.get("wish")=="again":
        request.session.pop("a",None)
        request.session.pop("b",None)
        request.session.pop("d",None)
        request.session.pop("e",None)
        request.session.pop("f",None)
        request.session.pop("g",None)
        request.session.pop("nog",None)
        guesses=None
        guess=None
        show=True
    if (request.POST.get("lrange") and request.POST.get("hrange")) or (request.POST.get("wish")=="again" and request.POST.get("lrange") and request.POST.get("hrange")):
        show=False
        if "a" not in request.session:
            request.session["a"]=int(request.POST.get("lrange"))
        if "b" not in request.session:
            request.session["b"]=int(request.POST.get("hrange"))
    if "a" in request.session and "b" in request.session:
        if "d" not in request.session:
            request.session["d"]=0
        if (request.POST.get("lrange") and request.POST.get("hrange")):
            if "e" not in request.session:
                request.session["e"]=request.session["b"]-request.session["a"]
        while "e" in request.session and request.session["e"]>1 and request.POST.get("lrange") and request.POST.get("hrange"):
            request.session["d"]+=1
            request.session["e"]=request.session["e"]/2
        if "f" not in request.session:
            request.session["f"]=0
        if "nog" not in request.session:
            request.session["nog"]="I'll do it in "+str(request.session["d"])+" guesses"
        if request.POST.get("loh"):
            if request.session["b"]-request.session["a"]>2:
                request.session["f"]+=1
                ges=request.session["f"]
                if request.POST.get("loh")=="low":
                    request.session["a"]=(request.session["b"]+request.session["a"])//2
                elif request.POST.get("loh")=="high":
                    request.session["b"]=(request.session["b"]+request.session["a"])//2
                elif request.POST.get("loh")=="correct":
                    guesses=str(request.session["f"])+" guesses"
                    mode=False
                if mode!=False:
                    request.session["g"]=(request.session["b"]+request.session["a"])//2
                    g=request.session["g"]
                    mode=True
            else:
                mode=False
                guess=str((request.session["a"]+request.session["b"])//2)+" in "+str(request.session["f"]+1)+" guesses"
        else:
            if "g" not in request.session:
                request.session["g"]=(request.session["b"]+request.session["a"])//2
            g=request.session["g"]
            mode=True
    context={"mode":mode,"guess":guess,"guesses":guesses,"nog":request.session.get("nog"),"g":g,"show":show,"ges":ges}
    return render(request,'myapp/computerguesses.html',context)
def gnav(request):
    return render(request,'myapp/guessingpage.html',{})
def clicker(request):
    #request.session["ach"]=[]
    one="""First click
    Get 1 click"""
    five="""Starter
    Get 5 clicks"""
    ten="""Decaclick
    Get 10 clicks"""
    fifty="""Half Century
    Get 50 clicks"""
    hundred="""Century
    Get 100 clicks"""
    thousand="""Wooden League
    Get 1000 clicks"""
    fivethousand="""Stone league
    Get 5000 clicks"""
    tenthousand="""Iron league
    Get 10000 clicks"""
    fiftythousand="""Gold league
    Get 50000 clicks"""
    hundredthousand="""Diamond league
    Get 100000 clicks"""
    thestarting="""The End?
    Get 500000 clicks"""
    theend="""The End
    Reach 1000000 clicks"""
    if "clicks" not in request.session:
        request.session["clicks"]=0
    if "ach" not in request.session:
        request.session["ach"]=[]
    heading="Click that button...please!"
    if request.method=="POST":
        if request.POST.get("play")=="again":
            request.session["clicks"]=0
        if request.POST.get("click")=="done":
            request.session["clicks"]+=1
        if request.POST.get("autoclick")=="yes" and request.session.get("tstate")=="unequip":
            request.session["clicks"]+=1
        if request.session["clicks"]==1:
            if ("1. "+one) not in request.session["ach"]:
                request.session["ach"].append("1. "+one)
            request.session.modified=True
        if request.session["clicks"]==5:
            if ("2. "+five) not in request.session["ach"]:
                request.session["ach"].append("2. "+five)
            request.session.modified=True
        if request.session["clicks"]==10:
            if ("3. "+ten) not in request.session["ach"]:
                request.session["ach"].append("3. "+ten)
            request.session.modified=True
        if request.session["clicks"]==50:
            if ("4. "+fifty) not in request.session["ach"]:
                request.session["ach"].append("4. "+fifty)
            request.session.modified=True
        if request.session["clicks"]==100:
            if ("5. "+hundred) not in request.session["ach"]:
                request.session["ach"].append("5. "+hundred)
            request.session.modified=True
        if request.session["clicks"]==1000:
            if ("6. "+thousand) not in request.session["ach"]:
                request.session["ach"].append("6. "+thousand)
            request.session.modified=True
        if request.session["clicks"]==5000:
            if ("7. "+fivethousand) not in request.session["ach"]:
                request.session["ach"].append("7. "+fivethousand)
            request.session.modified=True
        if request.session["clicks"]==10000:
            if ("8. "+tenthousand) not in request.session["ach"]:
                request.session["ach"].append("8. "+tenthousand)
            request.session.modified=True
        if request.session["clicks"]==50000:
            if ("9. "+fiftythousand) not in request.session["ach"]:
                request.session["ach"].append("9. "+fiftythousand)
            request.session.modified=True
        if request.session["clicks"]==100000:
            if ("10. "+hundredthousand) not in request.session["ach"]:
                request.session["ach"].append("10. "+hundredthousand)
            request.session.modified=True
        if request.session["clicks"]==500000:
            if ("11. "+thestarting) not in request.session["ach"]:
                request.session["ach"].append("11. "+thestarting)
            request.session.modified=True
        if request.session["clicks"]==1000000:
            if ("12. "+theend) not in request.session["ach"]:
                request.session["ach"].append("12. "+theend)
            request.session.modified=True
        return redirect("clicker")
    context={"clicks":request.session["clicks"],"heading":heading,"ach":request.session["ach"],"tstate":request.session.get("tstate","buy")}
    return render(request,'myapp/earth.html',context)
def cach(request):
    if request.POST.get("restart")=="yes":
        request.session["ach"]=[]
    context={"ach":request.session.get("ach",[])}
    return render(request,'myapp/cach.html',context)
def equipment(request):
    if "clicks" not in request.session:
        request.session["clicks"]=0
    if "tstate" not in request.session:
        request.session["tstate"]="buy"
    if request.method=="POST":
        if request.POST.get("tshirt")=="yes" and ((request.session["tstate"]=="buy" and request.session["clicks"]>=50) or request.session["tstate"]=="equip"):
            if request.session["tstate"]=="buy":
                if request.session["clicks"]>=50:
                    request.session["tstate"]="unequip"
                    request.session["clicks"]-=50
            elif request.session["tstate"]=="equip":
                request.session["tstate"]="unequip"
        elif request.POST.get("autoclick")=="yes" and request.session["tstate"]=="unequip":
            request.session["clicks"]+=1
        elif request.POST.get("tshirt")=="yes" and request.session["tstate"]=="unequip":
            request.session["tstate"]="equip"
        elif request.POST.get("sell")=="yes" and request.session["tstate"]!="buy":
            request.session["tstate"]="buy"
            request.session["clicks"]+=50
    context={"tstate":request.session["tstate"],"clicks":request.session["clicks"]}
    return render(request,'myapp/equipment.html',context)
from django.http import JsonResponse

def get_clicks(request):
    return JsonResponse({"clicks": request.session.get("clicks", 0)})