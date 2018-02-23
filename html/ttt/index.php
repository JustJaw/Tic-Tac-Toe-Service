
<head>
    <style>
        #theContent {
            margin-top:5%;
            text-align:center;
            /*margin: auto 0;*/
        }
    </style>
</head>
<pre>
<!--#echo var="DATE_LOCAL" -->
</pre>

<form action="" method="post">
    Name:
    <input type="text" name="name" required>
    <br>
    <input type="submit" value="Submit">
</form>

<br/>
<?php
if($_POST["name"]) {
    echo "Welcome " . $_POST["name"] . ", " . date("F j, Y, g:i a"); 
}
?>
<br>
<br/>
<div id="theContent">
    
    <div id ="The board">
    <table id= "tictactoe" style="border:2px solid red; width : 50%; height: 50%">
            <tr>
                <td id='g-0' class="clickGrid" style="border:2px solid black"></td>
                <td id='g-1' class="clickGrid" style="border:2px solid black">

    </td>
                <td id='g-2' class="clickGrid" style="border:2px solid black">

    </td>
            </tr>
            <tr>
                <td id='g-3' class="clickGrid" style="border:2px solid black">

    </td>
                <td id='g-4' class="clickGrid" style="border:2px solid black">

    </td>
                <td id='g-5' class="clickGrid" style="border:2px solid black">

    </td>
            </tr>
            <tr>
                <td id='g-6' class="clickGrid" style="border:2px solid black">

    </td>
                <td id='g-7' class="clickGrid" style="border:2px solid black">

    </td>
                <td id='g-8' class="clickGrid" style="border:2px solid black">

    </td>
            </tr>
    </table>
    </div>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script>

    //Empty Space
    var E = " "

    var X = "X"
    var O = "O"

    var grid = [E, E, E,
                E, E, E,
                E, E, E]

    
    $(".clickGrid").click(function() {
        
        var idSelected =$(this).attr('id').slice(2); 	

        if (grid[idSelected]===E){

            grid[idSelected] = X
            
            playMove();
        }
        else{
            alert("You clicked a field aleady selected")
        }

    });

    var placeMove = function(player, move){
        
    }

    var playMove = function() {
        
        var theData = {
            "grid" : grid,
            "winner": E  
        } 
        

        $.ajax({
            type: "POST",
            url: "http://130.245.171.42/ttt/play",
            data: JSON.stringify(theData),
            success: function (data) {
                winner = data.winner;
                serverMove = data.move;
                grid[serverMove] = O

                if(winner == X || winner == O) {
                    alert(winner + " WINS!")
                }
                else if(w)
            },
            error: function (data) {
                console.log(data)
            },
            dataType: "JSON",
            contentType: "application/json; charset=utf-8",
        });
    };
</script>
