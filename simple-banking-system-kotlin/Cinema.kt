package cinema


class Seat(val cost: Int) {
    private var symbol = "S"

    override fun toString(): String {
        return symbol
    }

    fun reserve() {
        symbol = "B"
    }

    fun alreadyReserved(): Boolean {
        return symbol == "B"
    }
}

class CinemaRoom(private val rows: Int, private val seatsInRow: Int) {
    private val size = rows * seatsInRow
    private val seats = fillSeats()


    override fun toString(): String {
        var cinemaString = "Cinema:\n  "

        //printing upper seat numbers
        val upperSeatNumbers = Array(seatsInRow) { index: Int -> index + 1 }
        cinemaString += "${upperSeatNumbers.joinToString(" ")}\n"

        for ((index, row) in seats.withIndex()) {
            cinemaString += "${index + 1} ${row.joinToString(" ")}\n"
        }

        return cinemaString
    }

    private fun fillSeats(): Array<Array<Seat>> {
        return if (size < 60) fillLittleRoom() else fillBigRoom()
    }

    private fun fillLittleRoom(): Array<Array<Seat>> {
        return Array(rows) { Array(seatsInRow) { Seat(10) } }
    }

    private fun fillBigRoom(): Array<Array<Seat>> {
        return Array(rows) { row ->
            Array(seatsInRow) {
                if (row < rows / 2) Seat(10) else Seat(8)
            }
        }
    }

    private fun showStatistic() {
        var purchasedTicketsNumber = 0
        var currentIncome = 0
        var totalIncome = 0
        for (seatsInRow in seats) {
            seatsInRow.forEach { totalIncome += it.cost }

            val reservedSeatsInRow = seatsInRow.filter { it.alreadyReserved() }
            purchasedTicketsNumber += reservedSeatsInRow.size
            reservedSeatsInRow.forEach { currentIncome += it.cost }
        }

        val purchasedTicketsPercentage = purchasedTicketsNumber.toDouble() / size * 100
        val formatPurchasedTicketsPercentage = "%.2f".format(purchasedTicketsPercentage)
        println("Number of purchased tickets: $purchasedTicketsNumber")
        println("Percentage: ${formatPurchasedTicketsPercentage}%")
        println("Current income: $${currentIncome}")
        println("Total income: $${totalIncome}\n")
    }

    fun printMenu() {
        while (true) {
            println("1. Show the seats")
            println("2. Buy a ticket")
            println("3. Statistics")
            println("0. Exit")

            when (readln().toInt()) {
                1 -> println(this)
                2 -> reserveSeat()
                3 -> showStatistic()

                else -> break
            }
        }
    }

    private fun reserveSeat() {
        fun chooseSeat(): Seat {
            println("Enter a row number:")
            val rowPosition = readln().toInt()

            println("Enter a seat number in that row:")
            val seatPosition = readln().toInt()

            return seats[rowPosition - 1][seatPosition - 1]
        }

        while (true) {
            try {
                val chosenSeat = chooseSeat()
                if (chosenSeat.alreadyReserved()) {
                    println("That ticket has already been purchased!\n")
                    continue
                }
                chosenSeat.reserve()
                println("Ticket price: $${chosenSeat.cost}\n")
                break
            } catch (e: IndexOutOfBoundsException) {
                println("Wrong input!\n")
            }
        }
    }
}

fun main() {
    println("Enter the number of rows:")
    val rows = readln().toInt()

    println("Enter the number of seats in each row:")
    val seats = readln().toInt()

    if (rows < 0 || seats < 0) {
        println("the number of seats cannot be negative")
        return
    }

    val cinemaRoom = CinemaRoom(rows, seats)
    cinemaRoom.printMenu()
}
