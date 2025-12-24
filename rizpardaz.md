#include <avr/io.h>
#include <avr/interrupt.h>

ISR(TIMER1_COMPA_vect)
{
    PORTB ^= (1 << PB5); 
}

void setup()
{
    DDRB |= (1 << PB5);

    TCCR1A = 0x00;         
    TCCR1B = 0x0C;         

    OCR1A = 62500;         

    TIMSK1 |= (1 << OCIE1A); 

    sei();  
}

void loop()
{
   
}
