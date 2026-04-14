package factory;

import model.resource.Resource;
import model.transaction.*;
import model.user.Student;

import java.time.LocalDate;

public class TransactionFactory {

    public static Transaction createTransaction(
            String type,
            Resource resource,
            Student firstStudent,
            Student secondStudent,
            double price
    ) {

        switch (type.toUpperCase()) {

            case "BUYSELL":
                return new BuySellTransaction(
                        0,
                        resource,
                        firstStudent,
                        secondStudent,
                        price
                );

            case "LENDBORROW":
                return new LendBorrowTransaction(
                        0,
                        resource,
                        firstStudent,
                        secondStudent,
                        LocalDate.now(),
                        LocalDate.now().plusDays(7)
                );

            default:
                throw new IllegalArgumentException("Invalid transaction type.");
        }
    }

    public static Transaction createBarterTransaction(
            Resource offered,
            Resource requested,
            Student proposer,
            Student accepter
    ) {
        return new BarterTransaction(
                0,
                offered,
                requested,
                proposer,
                accepter
        );
    }
}