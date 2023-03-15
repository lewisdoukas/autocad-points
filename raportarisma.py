import sys
import ezdxf
import pandas as pd



def help():
    print("Text file format:  id,x,y,H")
    print("e.g:\n1,500650.590,4204238.460,351.234\n2,500650.920,4204252.530,350.582")
    print("\nExecution:\npython raportarisma.py coords_filename layer_name")
    print("e.g:\npython raportarisma.py coords.txt apotiposi")


def raportarisma(input_filename, layer_name):
    def add_point(df, msp):
        index = df.name
        blockname = layer_name + f"_block{index}"
        block = doc.blocks.new(name= blockname, base_point=(df['x'], df['y']))

        msp.add_blockref(blockname, (df['x'], df['y']), dxfattribs= {"layer": layer_name})
        p = block.add_point((df['x'], df['y']), dxfattribs= {"layer": layer_name})


        block.add_text(df['id'], dxfattribs= {
            "layer": layer_name + "_id",
            "style": "LiberationSerif",
            "height": 0.3 }).set_pos((df['x'] + 0.1, df['y'] + 0.17), align= "LEFT")

        block.add_text(df['h'], dxfattribs= {
            "layer": layer_name + "_height",
            "style": "LiberationSerif",
            "height": 0.3 }).set_pos((df['x'] + 0.1, df['y'] - 0.17), align= "LEFT")


    doc = ezdxf.new(dxfversion= "R2010", setup= True)    
    doc.header['$PDSIZE'] = -1
    doc.header['$PDMODE'] = 33 # circle 2 for cross

    doc.layers.new(layer_name + "_id", dxfattribs={"color": 7}) 
    doc.layers.new(layer_name, dxfattribs={"color": 7}) 
    doc.layers.new(layer_name + "_height", dxfattribs={"color": 7}) 
    msp = doc.modelspace()

    df = pd.read_csv(input_filename, header= None, names= ["id", "x", "y", "h"])
    df['id'] = df['id'].astype(str)

    df.apply(add_point, axis= 1, args= [msp])

    doc.saveas(f"raportarisma_{layer_name}.dxf", encoding= "utf-8")
    print("Raportarisma done!")



def main():
    arg1 = sys.argv[1]

    if arg1 == "help" or arg1 == "--h" or arg1 == "-h":
        help()
    else:
        input_filename  = arg1
        layer_name = sys.argv[2]
        raportarisma(input_filename, layer_name)

if __name__ == "__main__":
    main()

    