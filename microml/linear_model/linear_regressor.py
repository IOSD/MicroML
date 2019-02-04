import keras
from sklearn.linear_model import LinearRegression
import serial

class Linear_Model:
    ino_base = """
    void setup() {{
        Serial.begin(9600);
    }}

    float f[{count}];
    void loop() {{
    if(Serial.available()>0){{
        for(int i=0;i<{count};i++)  f[i] = get_float();
        float w[{count}]={{ {weights} }};
        float b = {intercept};
        float s = b;

        for(int i=0;i<{count};i++)s+= f[i]*w[i]; 

        Serial.println(s);
        }}
    }}

    float get_float(){{
        float incoming_value;
        unsigned char buffer[4];
        if (Serial.readBytes(buffer, sizeof(float)) == sizeof(float))
                memcpy(&incoming_value, buffer, sizeof(float));
        else
                incoming_value = 0;
        return incoming_value;
    }}
    """

    def __init__(self,port,baudrate):
        self.port = port
        self.baudrate = baudrate

    def predict(self,input):
        ser = serial.Serial(self.port,self.baudrate)
        s = b''
        for inp in input:
            s+=struct.pack('f',inp)
        ser.write(s);
        result = ser.readline()
        ser.close()

        return result
    

    def generate_ino(self,model):
        if not isinstance(model,LinearRegression):
            raise ValueError("Model Provided was not a Linear Model")
        weights_str = ", ".join([ str(i) for i in model.coef_])
        with open("model.ino",'w') as f:
            f.write(self.ino_base.format(count=len(model.coef_),weights=weights_str,intercept=model.intercept_))